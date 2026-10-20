"""Implement the reviewed CAT-TC01..33. Live actions require --execute.

Fixture preparation is external to this runner. SQLite is opened read-only;
Web cases use the real Admin UI, API cases send one target request each.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from contextlib import ExitStack, closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler


FEATURE = Path(__file__).resolve().parents[1]
REPO = FEATURE.parents[2]
ADMIN_URL = "http://localhost:5174/"
API_URL = "http://localhost:3000/api"
CREDENTIALS = {
    "admin": {"email": "admin@eshop.com", "password": "Admin123!"},
    "user": {"email": "test@eshop.com", "password": "Test1234!"},
}


class Blocked(RuntimeError):
    """A precondition/observation cannot be established; no pass is inferred."""


class Failure(AssertionError):
    """The observed target behavior contradicts the documented oracle."""


class TransportError(Blocked):
    """Stop the batch: a submitted request may have had an unknown outcome."""


def now():
    return datetime.now(timezone.utc).isoformat()


def check(condition, message):
    if not condition:
        raise Failure(message)


def digest(path):
    # Normalize only Git line endings, never the strings used as test input.
    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()


def load_catalogue():
    data = json.loads((FEATURE / "scripts/cases.json").read_text(encoding="utf-8"))
    if data.get("design_version") != "0.2" or data.get("schema_version") != 1:
        raise Blocked("Unsupported design/catalogue version")
    for name in ("design.md", "test-cases.md"):
        if digest(FEATURE / name) != data["documents"][name]:
            raise Blocked(f"Reviewed {name} changed; reconcile the catalogue first")
    if [c["id"] for c in data["cases"]] != [f"CAT-TC{i:02}" for i in range(1, 34)]:
        raise Blocked("Each CAT-TC01..33 must occur exactly once")
    return data


def decode64(value):
    return base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)


def encode64(value):
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def altered_payload(token):
    header, payload, signature = token.split(".")
    claims = json.loads(decode64(payload))
    if claims.get("role") != "user":
        raise Blocked("TP must start from the original user token")
    claims["role"] = "admin"
    changed = encode64(json.dumps(claims, ensure_ascii=False, separators=(",", ":")).encode())
    return ".".join((header, changed, signature))


def altered_signature(token):
    header, payload, signature = token.split(".")
    changed = bytearray(decode64(signature))
    if not changed:
        raise Blocked("The original admin token has no signature bytes")
    changed[0] ^= 0x01
    return ".".join((header, payload, encode64(changed)))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class API:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.opener = build_opener(ProxyHandler({}), NoRedirect())
        self.tokens = {}

    def request(self, method, path, token=None, body=None):
        headers = {"Content-Type": "application/json"}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        request = Request(self.url + path, method=method, headers=headers,
                          data=None if body is None else json.dumps(body, ensure_ascii=False).encode())
        try:
            response = self.opener.open(request, timeout=10)
        except HTTPError as error:
            response = error
        except (URLError, TimeoutError, OSError) as error:
            raise TransportError(f"HTTP transport failed for {method} {path}") from error
        with response:
            try:
                raw = response.read().decode("utf-8")
            except (OSError, UnicodeError) as error:
                raise TransportError(f"Cannot read {method} {path} response") from error
            try:
                body = json.loads(raw)
            except ValueError:
                body = raw
            return {"status": response.code, "body": body}

    def token(self, role):
        if role not in self.tokens:
            response = self.request("POST", "/login", body=CREDENTIALS[role])
            body = response["body"]
            if not 200 <= response["status"] < 300 or not isinstance(body, dict):
                raise Blocked(f"Cannot authenticate the nominal {role} account")
            if body.get("user", {}).get("role") != role or not isinstance(body.get("token"), str):
                raise Blocked(f"Login did not issue the expected {role} identity")
            self.tokens[role] = body["token"]
        token = self.tokens[role]
        verification = self.request("GET", "/users/me", token)
        me = verification["body"]
        if (not 200 <= verification["status"] < 300 or not isinstance(me, dict)
                or me.get("role") != role or me.get("email") != CREDENTIALS[role]["email"]):
            raise Blocked(f"GET /users/me did not verify the original {role} token")
        # Never store login or /users/me response bodies: they may contain passwords/tokens.
        return token

    def categories(self, token):
        result = self.request("GET", "/categories", token)
        if not 200 <= result["status"] < 300:
            raise Blocked("Cannot observe categories through GET")
        return category_rows(result["body"])


def category_rows(value):
    if not isinstance(value, list) or any(not isinstance(r, dict) or "id" not in r or "name" not in r for r in value):
        raise Blocked("Category observation is not a list of id/name records")
    ids = [r["id"] for r in value]
    if len(ids) != len(set(ids)):
        raise Failure("Duplicate category IDs in observation")
    return sorted(({"id": r["id"], "name": r["name"]} for r in value), key=lambda r: r["id"])


class Database:
    def __init__(self, path):
        self.path = Path(path).resolve(strict=True)
        if self.path.is_relative_to(REPO):
            raise Blocked("Select an isolated runtime DB outside the repository")

    def snapshot(self):
        with closing(sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True, timeout=3)) as db:
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA query_only=ON")
            db.execute("BEGIN")
            rows = [dict(r) for r in db.execute("SELECT id,name FROM categories ORDER BY id")]
            refs = {r[0]: r[1] for r in db.execute(
                "SELECT category_id,COUNT(*) FROM products GROUP BY category_id")}
            users = [dict(r) for r in db.execute(
                "SELECT id,email,role FROM users WHERE email IN (?,?)",
                (CREDENTIALS["admin"]["email"], CREDENTIALS["user"]["email"]))]
        return {"categories": category_rows(rows), "references": refs, "users": users}

    def fixture(self, case, catalogue):
        snapshot = self.snapshot()
        rows = snapshot["categories"]
        if Counter(r["name"] for r in rows) != Counter(catalogue["fixtures"][case["fixture"]]):
            raise Blocked(f"Prepare {case['fixture']} externally; the current dataset is different")
        if any(snapshot["references"].get(r["id"], 0) for r in rows):
            raise Blocked("Fixture categories must have no product references")
        roles = ["admin"]
        if case.get("auth") in ("TU", "TP") or case.get("entry") in ("login_user", "stored_user"):
            roles.append("user")
        for role in roles:
            credentials = CREDENTIALS[role]
            matching = [u for u in snapshot["users"] if u["email"] == credentials["email"]]
            if len(matching) != 1 or matching[0]["role"] != role:
                raise Blocked(f"Nominal {role} account is missing or has the wrong role")
        ids = {"i" + str(i + 1): next(r["id"] for r in rows if r["name"] == name)
               for i, name in enumerate(catalogue["fixtures"][case["fixture"]])}
        ids["missing"] = 999999
        existing = {r["id"] for r in rows}
        while ids["missing"] in existing:
            ids["missing"] += 1
        return rows, ids


class Web:
    """One fresh browser context per TC, real UI submits, no API stubbing."""

    def __init__(self, browser, url, api_url, observation, timeout):
        self.context = browser.new_context(viewport={"width": 1280, "height": 800})
        self.url, self.api_url = url, api_url.rstrip("/")
        self.timeout, self.observation = timeout, observation
        self.pending = set()
        self.category_responses = []
        self.last_network_change = time.monotonic()
        self.page = self.new_page()

    def new_page(self):
        page = self.context.new_page()
        page.set_default_timeout(self.timeout)
        page.on("dialog", self.dialog)
        page.on("request", lambda r: self.network(r, True))
        page.on("requestfinished", lambda r: self.network(r, False))
        page.on("requestfailed", lambda r: self.network(r, False))
        page.on("response", self.response)
        return page

    def response(self, response):
        if response.url == self.api_url + "/categories" and response.request.method == "GET":
            self.category_responses.append(response)

    def network(self, request, started):
        if request.url.startswith(self.api_url + "/"):
            if started:
                self.pending.add(id(request))
            else:
                self.pending.discard(id(request))
            self.last_network_change = time.monotonic()

    def settle(self):
        # Wait for the observed bootstrap/refresh requests, not a business-time boundary.
        if not self.poll(lambda: not self.pending and time.monotonic() - self.last_network_change >= 0.1):
            raise TransportError("Admin API requests have not settled; target outcome may be unknown")

    def dialog(self, dialog):
        self.observation.setdefault("dialogs", []).append({"type": dialog.type, "message": dialog.message})
        if dialog.type == "confirm":
            dialog.accept()
        else:
            dialog.dismiss()

    def poll(self, predicate):
        deadline = time.monotonic() + self.timeout / 1000
        while True:
            if predicate():
                return True
            if time.monotonic() >= deadline:
                return False
            self.page.wait_for_timeout(50)  # Pump real browser events while polling a condition.

    def open(self):
        self.page.goto(self.url, wait_until="domcontentloaded")
        if not self.poll(lambda: self.page.get_by_placeholder("Email", exact=True).is_visible()
                         or self.page.get_by_text("Danh mục", exact=True).is_visible()):
            raise Blocked("Admin page did not reach an identifiable state")
        self.settle()

    def login(self, role):
        self.open()
        credentials = CREDENTIALS[role]
        self.page.get_by_placeholder("Email", exact=True).fill(credentials["email"])
        self.page.get_by_placeholder("Password", exact=True).fill(credentials["password"])
        responses = []
        start_dialogs = len(self.observation.get("dialogs", []))
        listener = lambda r: responses.append(r) if r.url == self.api_url + "/login" and r.request.method == "POST" else None
        self.page.on("response", listener)
        try:
            self.page.get_by_role("button", name="Login", exact=True).click()
            if not self.poll(lambda: bool(responses)):
                raise Blocked("Cannot observe the Web login request")
            response = responses[0]
            payload = response.json()
            if not response.ok or payload.get("user", {}).get("role") != role:
                raise Blocked(f"Web login did not authenticate the nominal {role} account")
            self.observation["login_identity"] = {"email": credentials["email"], "role": role}
            self.poll(lambda: self.page.get_by_text("Danh mục", exact=True).is_visible()
                      or len(self.observation.get("dialogs", [])) > start_dialogs)
            self.settle()
            if role == "admin" and not self.poll(lambda: self.page.get_by_text("Danh mục", exact=True).is_visible()):
                raise Blocked("PA unavailable: valid admin cannot open the category navigation")
        finally:
            self.page.remove_listener("response", listener)

    def panel(self):
        self.page.get_by_text("Danh mục", exact=True).click()
        self.page.get_by_role("heading", name="Quản lý Danh mục", exact=True).wait_for()

    def rows(self):
        rows = []
        for row in self.page.locator("table tbody tr").all():
            cells = row.locator("td").all_text_contents()
            if len(cells) < 2 or not re.fullmatch(r"#\d+", cells[0].strip()):
                raise Failure("Category table has an unreadable ID/name row")
            rows.append({"id": int(cells[0].strip()[1:]), "name": cells[1]})
        return category_rows(rows)

    def assert_rows(self, expected, key):
        self.settle()
        if not self.category_responses:
            raise Blocked("No category-list response observed in the browser")
        response = self.category_responses[-1]
        check(response.ok, "Web category-list request failed")
        fetched = category_rows(response.json())
        self.observation.setdefault("web_category_reads", []).append(
            {"status": response.status, "categories": fetched})
        check(fetched == expected, "Web fetched a different category set from the fixture/persistence")
        self.poll(lambda: self.rows() == expected)
        actual = self.rows()
        self.observation[key] = actual
        check(actual == expected, f"Web table {key} differs from the expected id/name set")

    def reload_panel(self):
        previous = len(self.category_responses)
        self.page.reload(wait_until="domcontentloaded")
        self.settle()
        self.panel()
        if not self.poll(lambda: len(self.category_responses) > previous):
            raise Blocked("Cannot confirm the category list was loaded after reload")
        self.settle()

    def mutate(self, case, ids):
        method = "POST" if case["kind"] == "web_add" else "DELETE"
        path = "/categories" if method == "POST" else "/categories/" + str(ids[case["target"]])
        responses = []
        requests = []
        listener = lambda r: responses.append(r) if r.url == self.api_url + path and r.request.method == method else None
        request_listener = lambda r: requests.append(r) if r.url == self.api_url + path and r.method == method else None
        self.page.on("response", listener)
        self.page.on("request", request_listener)
        start_dialogs = len(self.observation.get("dialogs", []))
        self.observation["target_request"] = {"method": method, "path": path, "response": None}
        try:
            if method == "POST":
                field = self.page.get_by_placeholder("Tên danh mục mới", exact=True)
                field.fill(case["name"])
                if field.input_value() != case["name"]:
                    raise Blocked("Cannot establish the literal name input required by the TC")
                button = self.page.get_by_role("button", name="Thêm mới", exact=True)
            else:
                row = self.page.locator("table tbody tr").filter(
                    has=self.page.get_by_role("cell", name="#" + str(ids[case["target"]]), exact=True))
                button = row.get_by_role("button", name="Xóa", exact=True)
            button.click()  # Exactly one target UI submit; no automatic mutation retry.
            self.poll(lambda: bool(responses)
                      or (method == "POST" and len(self.observation.get("dialogs", [])) > start_dialogs)
                      or (method == "POST" and bool(self.page.get_by_role("alert").all_text_contents()))
                      or (method == "POST" and field.evaluate("e => !e.validity.valid")))
            native_invalid = method == "POST" and field.evaluate("e => !e.validity.valid")
            self.observation["native_validation"] = bool(native_invalid)
            inline = self.page.get_by_role("alert").all_text_contents()
            self.observation["inline_feedback"] = inline
            if len(requests) > 1:
                raise TransportError("Multiple target requests observed for one UI submit")
            response = responses[0] if responses else None
            reply = None
            if response:
                try:
                    body = response.json()
                except Exception:
                    body = response.text()
                reply = {"status": response.status, "body": body}
                if method == "POST" and response.request.post_data_json != {"name": case["name"]}:
                    raise Failure("Web submitted a different name from the reviewed input")
            messages = inline + [d["message"] for d in self.observation.get("dialogs", [])[start_dialogs:]]
            feedback = bool(native_invalid or any(re.search(
                r"lỗi|không|thiếu|bắt buộc|trống|vui lòng|hãy nhập|invalid|error|fail|required|empty|reject|please|must|cannot|unable",
                message, re.I) for message in messages))
            self.observation["target_request"] = {"method": method, "path": path, "response": reply}
            if requests and response is None:
                raise TransportError("Target request was sent but its response was not observed")
            self.settle()
            return reply, feedback
        finally:
            self.page.remove_listener("response", listener)
            self.page.remove_listener("request", request_listener)

    def access_state(self, key):
        self.settle()
        self.poll(lambda: self.page.get_by_placeholder("Email", exact=True).is_visible()
                  or self.page.get_by_text("Danh mục", exact=True).is_visible())
        nav = self.page.get_by_text("Danh mục", exact=True)
        if nav.is_visible():
            nav.click()
        panel = self.page.get_by_role("heading", name="Quản lý Danh mục", exact=True)
        # A visible management navigation is already access to the Admin subsystem.
        self.poll(lambda: panel.is_visible() or self.page.get_by_placeholder("Email", exact=True).is_visible())
        state = {"category_navigation": nav.is_visible(), "category_panel": panel.is_visible(),
                 "create_control": self.page.get_by_role("button", name="Thêm mới", exact=True).is_visible(),
                 "login_form": self.page.get_by_placeholder("Email", exact=True).is_visible(),
                 "body": self.page.locator("body").inner_text()}
        self.observation[key] = state
        return state

    def close(self):
        self.context.close()


def accepted(reply):
    if reply is None or not 200 <= reply["status"] < 300:
        return False
    body = reply["body"]
    return not (isinstance(body, dict) and (body.get("error") or body.get("success") is False))


def auth_rejected(reply):
    if reply is None or accepted(reply):
        return False
    feedback = json.dumps(reply["body"], ensure_ascii=False).lower()
    return reply["status"] in (401, 403) or bool(re.search(
        r"unauthor|forbid|token|jwt|admin|permission|quyền|xác thực|đăng nhập|không được phép|access denied", feedback))


def assert_access_denied(states, observation):
    for state in states:
        check(not any(state[k] for k in ("category_navigation", "category_panel", "create_control")),
              "Non-admin session can reach category management")
        feedback = state["login_form"] or bool(observation.get("dialogs")) or bool(re.search(
            r"unauthor|forbid|admin|quyền|xác thực|đăng nhập", state["body"], re.I))
        check(feedback, "No authentication prompt or denial feedback is observable")


def execute_case(case, catalogue, database, api, browser, timeout, evidence_dir=None):
    result = {"id": case["id"], "status": "not_run", "started_at": now(),
              "input": case["input_text"], "expected": case["expected_text"],
              "traceability": case["traceability"], "observation": {}}
    obs = result["observation"]
    web = None
    stop = False
    try:
        before, ids = database.fixture(case, catalogue)
        obs.update(database_before=before, fixture_ids=ids)
        admin = api.token("admin")
        obs["api_before"] = api.categories(admin)
        if obs["api_before"] != before:
            raise Blocked("Runtime DB and API dataset differ before the target action")
        reply, feedback = None, False
        if case["kind"].startswith("web_"):
            web = Web(browser, ADMIN_URL, API_URL, obs, timeout)
            if case["kind"] == "web_access":
                if case["entry"] == "guest":
                    web.open()
                elif case["entry"] == "login_user":
                    api.token("user")  # Verify valid credentials separately from Admin UI.
                    web.login("user")
                else:
                    user = api.token("user")
                    web.open()
                    web.page.evaluate("token => localStorage.setItem('adminToken', token)", user)
                    web.page.close()
                    web.page = web.new_page()  # Same context, persisted localStorage, no Login submit.
                    web.open()
                states = [web.access_state("access_before_reload")]
                web.page.reload(wait_until="domcontentloaded")
                states.append(web.access_state("access_after_reload"))
            else:
                web.login("admin")
                web.panel()
                web.assert_rows(before, "ui_before")
                if case["kind"] != "web_view":
                    reply, feedback = web.mutate(case, ids)
                else:
                    web.reload_panel()
                    web.assert_rows(before, "ui_after_reload")
        else:
            tokens = {"none": None, "malformed": "not-a-jwt", "TA": admin}
            if case["auth"] in ("TU", "TP"):
                user = api.token("user")
                tokens[case["auth"]] = user if case["auth"] == "TU" else altered_payload(user)
            if case["auth"] == "TS":
                tokens["TS"] = altered_signature(admin)
            path = case["path"].format(**ids)
            reply = api.request(case["method"], path, tokens[case["auth"]], case["body"])
            obs["target_request"] = {"method": case["method"], "path": path,
                                     "token_variant": case["auth"], "body": case["body"], "response": reply}

        after = database.snapshot()["categories"]
        obs["database_after"] = after
        obs["api_after"] = api.categories(admin)
        if web and case["kind"] in ("web_add", "web_delete"):
            web.poll(lambda: web.rows() == after)
            obs["ui_after_action"] = web.rows()
            web.reload_panel()
            web.poll(lambda: web.rows() == after)
            obs["ui_after_reload"] = web.rows()
        check(obs["api_after"] == after, "API and persistence observations disagree after the action")
        oracle = case["oracle"]
        if oracle == "add":
            check(accepted(reply), "No acceptance response for a valid category")
            new = [r for r in after if r["id"] not in {x["id"] for x in before}]
            check(len(new) == 1 and new[0]["name"] == case["name"]
                  and [r for r in after if r not in new] == before,
                  "ADD-OK requires exactly one new id/name and unchanged old categories")
        elif oracle == "delete":
            check(accepted(reply), "No acceptance response for deletion")
            check(after == [r for r in before if r["id"] != ids[case["target"]]],
                  "Delete did not remove only the target category")
        else:
            check(after == before, "The category dataset changed unexpectedly")
            if oracle == "name_reject":
                check(not accepted(reply) and (feedback or reply is not None),
                      "NAME-REJECT requires failure/validation feedback and no success")
            elif oracle == "auth_reject":
                check(auth_rejected(reply), "AUTH-REJECT needs observable authentication/permission denial")
            elif oracle == "access_denied":
                assert_access_denied(states, obs)
            # TC24 deliberately asserts only unchanged categories, no status/message policy.

        if web and case["kind"] in ("web_add", "web_delete"):
            check(obs["ui_after_action"] == after, "Category UI differs from persistence after the action")
            check(obs["ui_after_reload"] == after, "Category UI differs from persistence after reload")
            web.assert_rows(after, "ui_after_reload")
        result["status"] = "passed"
    except Failure as error:
        result.update(status="failed", reason=str(error))
    except TransportError as error:
        result.update(status="blocked", reason=str(error))
        stop = True
    except (Blocked, sqlite3.Error, OSError, ValueError, KeyError) as error:
        result.update(status="blocked", reason=str(error))
    except Exception as error:
        result.update(status="blocked", reason=f"Harness error: {type(error).__name__}")
        stop = True
    finally:
        if result["status"] == "failed" and evidence_dir is not None:
            try:
                if web is None:
                    web = Web(browser, ADMIN_URL, API_URL, obs, timeout)
                    web.login("admin")
                    web.panel()
                    web.settle()
                    obs["evidence_view"] = "Read-only Admin view after the API action; request/token variant is evidenced by target_request, not by this screenshot"
                evidence_dir.mkdir(parents=True, exist_ok=True)
                image = evidence_dir / (case["id"] + "-actual.jpg")
                requested = now()
                web.page.screenshot(path=str(image), type="jpeg", quality=85, full_page=True)
                result["images"] = [{"path": "images/" + image.name,
                                     "capture_requested_at": requested, "capture_completed_by": now(),
                                     "state": "actual"}]
            except Exception as error:
                result["evidence_error"] = f"Screenshot unavailable: {type(error).__name__}"
        if web:
            try:
                web.close()
            except Exception:
                result["cleanup_error"] = "Browser context could not be closed"
                stop = True
        result["finished_at"] = now()
    return result, stop


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Explicitly enable live UI/API actions")
    parser.add_argument("--case", nargs="+", help="Selected CAT-TC IDs; external fixture must match each")
    parser.add_argument("--manifest", type=Path, help="T01 services.json for the actual isolated runtime DB")
    parser.add_argument("--output", type=Path, help="New JSON file for this future execution; never overwrite")
    parser.add_argument("--headed", action="store_true", help="Show the Chromium window")
    parser.add_argument("--timeout-ms", type=int, default=8000)
    args = parser.parse_args()
    catalogue = load_catalogue()
    chosen = args.case or [c["id"] for c in catalogue["cases"]]
    cases = {c["id"]: c for c in catalogue["cases"]}
    if len(chosen) != len(set(chosen)) or any(cid not in cases for cid in chosen):
        parser.error("Select distinct CAT-TC01..33 IDs")
    if not args.execute:
        for cid in chosen:
            print(f"{cid}: {cases[cid]['kind']} / {cases[cid]['oracle']} — Not Run")
        print("No --execute: no browser, HTTP, DB connection or output file was opened.")
        return 0
    if not args.manifest or not args.output or args.timeout_ms <= 0:
        parser.error("Execution needs --manifest, --output and a positive timeout")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    database = Database(manifest["backend_database"])
    if args.output.exists():
        parser.error("Output already exists; choose a new file to preserve run history")
    api = API(API_URL)
    run = {"started_at": now(), "design_version": catalogue["design_version"],
           "documents": catalogue["documents"], "manifest": str(args.manifest.resolve()),
           "selected": chosen, "cases": [{"id": cid, "status": "not_run"} for cid in chosen]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output, ExitStack() as stack:
        browser = None
        if any(cases[cid]["kind"].startswith("web_") for cid in chosen):
            from playwright.sync_api import sync_playwright
            playwright = stack.enter_context(sync_playwright())
            browser = playwright.chromium.launch(headless=not args.headed)
        try:
            for index, cid in enumerate(chosen):
                result, stop = execute_case(cases[cid], catalogue, database, api, browser, args.timeout_ms)
                run["cases"][index] = result
                output.seek(0)
                json.dump(run, output, ensure_ascii=False, indent=2)
                output.truncate()
                output.flush()
                print(cid + ": " + result["status"])
                if stop:
                    break
        finally:
            if browser:
                browser.close()
    return 1 if any(c["status"] != "passed" for c in run["cases"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
