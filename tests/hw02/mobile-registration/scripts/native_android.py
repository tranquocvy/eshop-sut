"""Native Android transport. No SUT interaction happens at import time."""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import time
import tempfile
from datetime import datetime, timezone


class HarnessError(RuntimeError):
    """A setup, input-delivery or observation problem; never a passing test."""


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def walk(value):
    if isinstance(value, list):
        for item in value:
            yield from walk(item)
    elif isinstance(value, dict):
        if "class" in value:
            yield value
        for key in ("content", "children"):
            yield from walk(value.get(key, []))


def app_nodes(tree):
    return [node for window in tree if window.get("type") == "APPLICATION"
            for node in walk(window.get("content", []))]


def label(value):
    return " ".join(value.replace("*", "").strip(" :").casefold().split())


def bounds(node):
    values = re.findall(r"-?\d+", node.get("bounds", ""))
    if len(values) != 4:
        raise HarnessError("UI node has no usable bounds")
    return tuple(map(int, values))


def visible(node, tree):
    if node.get("hidden") is True or node.get("visible-to-user") is False:
        return False
    x1, y1, x2, y2 = bounds(node)
    for window in tree:
        if window.get("type") != "APPLICATION":
            continue
        wx1, wy1, wx2, wy2 = bounds(window)
        if max(x1, wx1) < min(x2, wx2) and max(y1, wy1) < min(y2, wy2):
            return True
    return False


LABELS = {
    "họ tên": "name", "họ và tên": "name", "email": "email",
    "mật khẩu": "password", "xác nhận mật khẩu": "confirmation",
}


def fields(tree):
    """Bind a label to the next EditText, not to a fixed coordinate/index."""
    nodes = app_nodes(tree)
    found = {}
    for index, node in enumerate(nodes):
        role = LABELS.get(label(node.get("text", "")))
        if not role or node.get("class", "").endswith("EditText"):
            continue
        for candidate in nodes[index + 1:]:
            if LABELS.get(label(candidate.get("text", ""))):
                break
            if candidate.get("class", "").endswith("EditText"):
                if role in found and found[role] != candidate:
                    raise HarnessError(f"Ambiguous input binding: {role}")
                found[role] = candidate
                break
    return found


def texts(tree):
    return {node["text"] for node in app_nodes(tree)
            if node.get("text") and node.get("class", "").endswith("TextView")}


def is_registration(tree):
    return any(label(value) == "đăng ký tài khoản" for value in texts(tree))


def is_login(tree):
    values = {label(value) for value in texts(tree)}
    return (not is_registration(tree) and "đăng nhập" in values
            and ("quên mật khẩu?" in values or "sign in" in values))


class NativeAndroid:
    def __init__(self, sdk: Path, serial: str, expo_url: str,
                 package: str, evidence: Path, timeout: float = 30):
        self.sdk, self.serial = sdk, serial
        self.expo_url, self.package = expo_url, package
        self.evidence, self.timeout = evidence, timeout
        self.android = sdk / "cmdline-tools/latest/bin/android.exe"
        self.adb = sdk / "platform-tools/adb.exe"
        self.input_receipts = []
        self.submission_count = 0
        self.scratch = tempfile.TemporaryDirectory(prefix="mr-native-")
        self.pending_images = {}
        self.saved_images = []
        self.actions = []
        evidence.mkdir(parents=True, exist_ok=True)
        if not self.android.is_file() or not self.adb.is_file():
            raise HarnessError("Android CLI/adb not found in the selected SDK")

    def trace(self, event, **data):
        # Keep only bounded diagnostics in memory; never persist full UI trees.
        if event in {"command_error", "input_receipt"}:
            self.actions.append({"at": utc_now(), "event": event,
                                 **{k: v for k, v in data.items() if k != "tree"}})
            self.actions = self.actions[-6:]

    def begin_case(self):
        self.input_receipts = []
        self.submission_count = 0
        self.pending_images = {}
        self.saved_images = []
        self.actions = []

    def command(self, argv, *, binary=False):
        self.trace("command", argv=[str(item) for item in argv])
        try:
            result = subprocess.run([str(item) for item in argv],
                                    capture_output=True, timeout=self.timeout,
                                    check=False, shell=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            self.trace("command_error", error=str(error))
            raise HarnessError(f"Native command did not complete: {error}") from error
        self.trace("command_result", exit_code=result.returncode,
                   stdout=None if binary else result.stdout.decode("utf-8", "replace"),
                   stderr=result.stderr.decode("utf-8", "replace"))
        if result.returncode:
            raise HarnessError(f"Native command exit {result.returncode}: "
                               + result.stderr.decode("utf-8", "replace"))
        return result.stdout if binary else result.stdout.decode("utf-8", "replace")

    def cli(self, *args):
        return self.command([self.android, "--no-metrics", f"--sdk={self.sdk}", *args])

    def adb_command(self, *args, binary=False):
        return self.command([self.adb, "-s", self.serial, *args], binary=binary)

    def layout(self):
        # Read the UTF-8 file, not console text rendered through a Windows code page.
        path = Path(self.scratch.name) / "layout.json"
        self.cli("layout", f"--device={self.serial}", "--full", "--no-idle", f"--output={path}")
        try:
            tree = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as error:
            raise HarnessError(f"Cannot read native layout: {error}") from error
        if not isinstance(tree, list):
            raise HarnessError("Unexpected Android CLI layout schema")
        self.trace("layout", tree=tree)
        return tree

    def capture(self, name):
        # Hold input/feedback in memory until a failing assertion needs evidence.
        png = self.adb_command("exec-out", "screencap", "-p", binary=True)
        self.pending_images[name] = {"png": png, "captured_at": utc_now()}
        return name

    def save_failure_images(self, prefix):
        try:
            from PIL import Image
        except ImportError as error:
            raise HarnessError("Pillow is required to export real JPG evidence") from error
        # One input and one actual image, never a duplicate case-ended screenshot.
        names = list(self.pending_images)
        inputs = [n for n in names if n.endswith("-input")]
        actuals = [n for n in names if "dialog" in n or n == "confirmation-presence"]
        if not actuals:
            self.capture("failure-state")
            actuals = ["failure-state"]
        for kind, name in [("input", inputs[-1] if inputs else None), ("actual", actuals[-1])]:
            if name is None:
                continue
            saved = self.pending_images[name]
            jpg = self.evidence / f"{prefix}-{kind}.jpg"
            try:
                with Image.open(io.BytesIO(saved["png"])) as image:
                    if image.format != "PNG":
                        raise HarnessError("adb did not return a PNG screenshot")
                    size = image.size
                    with jpg.open("xb") as stream:
                        image.convert("RGB").save(stream, format="JPEG", quality=95)
                with Image.open(jpg) as image:
                    image.load()
                    if image.format != "JPEG" or image.size != size:
                        raise HarnessError("Screenshot export is not a valid JPEG")
            except (OSError, ValueError) as error:
                raise HarnessError(f"Cannot export screenshot evidence: {error}") from error
            self.saved_images.append({"path": "images/" + jpg.name, "state": kind,
                                      "captured_at": saved["captured_at"]})
        return self.saved_images

    def hide_keyboard(self):
        state = self.adb_command("shell", "dumpsys", "input_method")
        # The IME service keeps mIsInputViewShown=true after its window closes.
        # Only the input manager's current visibility may trigger Back; a second
        # Back would leave the SUT instead of dismissing a keyboard.
        if re.search(r"\bmInputShown=true\b", state):
            self.cli("input", f"--device={self.serial}", "key", "back")
            self.layout()

    def tap_node(self, node):
        x1, y1, x2, y2 = bounds(node)
        self.adb_command("shell", "input", "tap", str((x1 + x2) // 2),
                         str((y1 + y2) // 2))

    def tap_text(self, wanted, *, contains=False):
        tree = self.layout()
        candidates = []
        for node in app_nodes(tree):
            if "CLICKABLE" not in node.get("interactions", []) or not visible(node, tree):
                continue
            value = label(node.get("content-desc", node.get("text", "")))
            matches = label(wanted) in value if contains else label(wanted) == value
            if matches:
                candidates.append(node)
        if len(candidates) != 1:
            raise HarnessError(f"Expected one clickable {wanted!r}; found {len(candidates)}")
        self.tap_node(candidates[0])
        return self.layout()

    @staticmethod
    def fingerprint(tree):
        return json.dumps([(n.get("class"), n.get("text"), n.get("content-desc"),
                            n.get("bounds")) for n in app_nodes(tree)], ensure_ascii=False)

    def scroll(self, direction):
        tree = self.layout()
        containers = [n for n in app_nodes(tree)
                      if n.get("class", "").endswith("ScrollView") and visible(n, tree)]
        if not containers:
            return tree, False
        if len(containers) != 1:
            raise HarnessError("Ambiguous registration scroll container")
        x1, y1, x2, y2 = bounds(containers[0])
        x = (x1 + x2) // 2
        top, bottom = y1 + (y2-y1)//4, y2 - (y2-y1)//4
        start, end = (bottom, top) if direction == "down" else (top, bottom)
        self.adb_command("shell", "input", "swipe", str(x), str(start),
                         str(x), str(end), "300")
        after = self.layout()
        return after, self.fingerprint(after) != self.fingerprint(tree)

    def top(self):
        self.hide_keyboard()
        for _ in range(12):
            tree, moved = self.scroll("up")
            if not moved:
                return tree
        raise HarnessError("Could not establish the top of the form")

    def wait(self, predicate, description):
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            tree = self.layout()
            if predicate(tree):
                return tree
            time.sleep(0.2)
        raise HarnessError(f"Native screen not ready: {description}")

    def open_registration(self, *, restart):
        if restart:
            # Restart the client only: never clear Expo data, seed/reset DB or start backend.
            self.adb_command("shell", "cmd", "statusbar", "collapse")
            self.adb_command("shell", "am", "force-stop", self.package)
            # Expo Go can finish a cold deep-link LauncherActivity before its
            # experience store is ready. Initialize its launcher first; this is
            # app setup and never retries a Register submission.
            self.adb_command("shell", "am", "start", "-W", "-n",
                             f"{self.package}/.LauncherActivity")
            self.layout()
            self.adb_command("shell", "am", "start", "-W", "-a", "android.intent.action.VIEW",
                             "-d", self.expo_url, self.package)
            self.wait(lambda t: any(label(x) == "eshop mobile" for x in texts(t)),
                      "EShop loaded in Expo Go")
        self.hide_keyboard()
        tree = self.layout()
        if any(label(x).startswith("chào,") for x in texts(tree)):
            raise HarnessError("P0 requires a logged-out client")
        # Keep the client/session alive while following S: Home -> Login -> Register.
        self.tap_text("EShop Mobile")
        self.wait(lambda t: any(label(x) == "danh sách sản phẩm" for x in texts(t)), "Home")
        self.tap_text("Đăng nhập")
        self.wait(is_login, "Login")
        self.tap_text("Đăng ký ngay", contains=True)
        self.wait(is_registration, "Registration")

    def inspect_form(self):
        """Inspect the entire form, including controls below the first viewport."""
        tree = self.top()
        found = {}
        for _ in range(12):
            for role, node in fields(tree).items():
                if visible(node, tree):
                    found[role] = {"bounds": node.get("bounds"),
                                   "editable": "EDITABLE" in node.get("interactions", []),
                                   "class": node.get("class")}
            tree, moved = self.scroll("down")
            if not moved:
                self.top()
                return {"complete": True, "fields": found}
        raise HarnessError("Form inspection did not reach the end; absence is unproven")

    def locate_field(self, role):
        tree = self.top()
        for _ in range(12):
            node = fields(tree).get(role)
            if node and visible(node, tree):
                return node
            tree, moved = self.scroll("down")
            if not moved:
                break
        raise HarnessError(f"Cannot locate an editable {role} field")

    def set_field(self, role, value):
        node = self.locate_field(role)
        if "EDITABLE" not in node.get("interactions", []):
            raise HarnessError(f"Field {role} is not editable")
        self.tap_node(node)
        focused_tree = self.layout()
        focused_node = fields(focused_tree).get(role)
        if focused_node and not visible(focused_node, focused_tree):
            # Inline validation expands the form; the IME can hide a focused
            # password field. Dismiss IME, preserving focus, before replacement.
            self.hide_keyboard()
            focused_tree = self.layout()
            focused_node = fields(focused_tree).get(role)
        if not focused_node or not visible(focused_node, focused_tree):
            raise HarnessError(f"Focused {role} is not visible; no input or submit delivered")
        # Positional argv preserves empty strings, $, %, &, spaces and Unicode.
        # Do not use adb 'input text', shell quoting, %s, ASCII conversion or --submit.
        self.cli("input", f"--device={self.serial}", "text", value,
                 "class=EditText,focused=true", "--match=single", "--wait=1500")
        tree = self.layout()
        current = fields(tree).get(role)
        if not current:
            raise HarnessError(f"Field {role} disappeared after input")
        observed = current.get("text") or ""
        masked = "PASSWORD" in current.get("interactions", [])
        receipt = {"field": role, "requested": value,
                   "code_points": len(value), "utf16_units": len(value.encode("utf-16-le"))//2,
                   "sha256_utf8": hashlib.sha256(value.encode("utf-8")).hexdigest(),
                   "transport": "android input text / native replacement", "at": utc_now()}
        # Plaintext readback, when exposed, must not lose characters. SUT trim of
        # name/email is allowed by the reviewed normalization rules, not done here.
        if masked and (observed is None or not observed or
                       all(c in "•●*·" for c in observed)):
            receipt["readback"] = "masked: transport acknowledged; plaintext not exposed"
        else:
            allowed = [value, value.strip()] if role in ("name", "email") else [value]
            if observed not in allowed:
                raise HarnessError(f"Input readback differs for {role}; no submit performed")
            receipt["readback"] = observed
        self.input_receipts.append(receipt)
        self.trace("input_receipt", **receipt)
        self.hide_keyboard()

    def fill(self, values, form, *, password_only=False):
        roles = ["password"] if password_only else ["name", "email", "password"]
        if "confirmation" in form["fields"]:
            roles.append("confirmation")
        for role in roles:
            self.set_field(role, values[role])

    def submit(self, step):
        self.hide_keyboard()
        baseline = texts(self.top())
        for _ in range(12):
            tree = self.layout()
            buttons = [n for n in app_nodes(tree) if "CLICKABLE" in n.get("interactions", [])
                       and label(n.get("content-desc", n.get("text", ""))) == "đăng ký"
                       and visible(n, tree)]
            if len(buttons) == 1:
                self.capture(f"step-{step}-input")
                # Count delivery before sending: never retry an ambiguous submit.
                self.submission_count += 1
                self.tap_node(buttons[0])
                return self.observe(baseline, step)
            if len(buttons) > 1:
                raise HarnessError("Ambiguous Register submit button")
            _, moved = self.scroll("down")
            if not moved:
                break
        raise HarnessError("Register submit button not reachable")

    def observe(self, before_texts, step):
        deadline = time.monotonic() + self.timeout
        feedback = set()
        success_signal = False
        dialog_seen = False
        dialog_count = 0
        positioned = False
        while time.monotonic() < deadline:
            tree = self.layout()
            nodes = app_nodes(tree)
            dialog = [n for n in nodes if n.get("resource-id") in
                      {"android:id/alertTitle", "android:id/message"}]
            if dialog:
                dialog_seen = True
                dialog_count += 1
                if dialog_count > 3:
                    raise HarnessError("Feedback dialog did not settle after dismissal")
                messages = {n.get("text", "") for n in dialog} - {""}
                feedback.update(messages)
                self.capture(f"step-{step}-dialog-{dialog_count}")
                positive = " ".join(messages).casefold()
                negative = re.search(r"không.*thành công|thất bại|fail|error|lỗi", positive)
                success_signal = success_signal or (
                    bool(re.search(r"thành công|success", positive)) and not negative)
                primary = [n for n in nodes if n.get("resource-id") == "android:id/button1"]
                if len(primary) != 1:
                    raise HarnessError("Cannot dismiss native feedback dialog unambiguously")
                self.tap_node(primary[0])
                tree = self.layout()
                positioned = False
            if not positioned:
                tree = self.top()
                positioned = True
            # A dialog may appear during the scroll-to-top/layout operation.
            # Handle/dismiss it on the next iteration, not as inline validation.
            if any(n.get("resource-id") in {"android:id/alertTitle", "android:id/message"}
                   for n in app_nodes(tree)):
                continue
            added = texts(tree) - before_texts
            # Login labels are state, not validation error feedback.
            if is_registration(tree):
                feedback.update(added)
                # The same validation message can remain visible across attempts.
                # Its presence after submit is evidence even when no text changed.
                feedback.update(value for value in texts(tree) if re.search(
                    r"mật khẩu quá yếu|không hợp lệ|đăng ký thất bại", value.casefold()))
            joined = " ".join(feedback).casefold()
            if (re.search(r"thành công|success", joined)
                    and not re.search(r"không.*thành công|thất bại|fail|error|lỗi", joined)):
                success_signal = True
            if re.search(r"network request failed|failed to fetch|fetch failed|connection refused|"
                         r"unable to resolve host|không thể kết nối|networkerror", joined):
                raise HarnessError("Native feedback indicates a connection/setup problem")
            if is_login(tree) or feedback:
                return {"at": utc_now(), "feedback": sorted(feedback),
                        "success_signal": success_signal, "dialog_seen": dialog_seen,
                        "login": is_login(tree), "registration": is_registration(tree),
                        "timed_out": False}
            time.sleep(0.2)
        tree = self.layout()
        return {"at": utc_now(), "feedback": sorted(feedback),
                "success_signal": success_signal, "dialog_seen": dialog_seen,
                "login": is_login(tree), "registration": is_registration(tree),
                "timed_out": True}
