"""Implement MR-TC01..54 through native UI; execute only with --execute.

The JSON catalogue contains fixed expected outcomes from the reviewed docs.
This runner never derives expected outcomes from the SUT password validator.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import time
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

from native_android import HarnessError, NativeAndroid, utc_now


FEATURE = Path(__file__).resolve().parents[1]
REPO = FEATURE.parents[2]


class CaseFailure(RuntimeError):
    """An observed outcome does not meet the documented expected outcome."""


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        raise HarnessError(f"Cannot read JSON {path}: {error}") from error


def document_digest(path):
    # Ignore Git's CRLF/LF conversion, never normalize test input strings.
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def load_catalogue(namespace):
    data = read_json(FEATURE / "scripts/cases.json")
    if data.get("schema_version") != 1 or data.get("design_version") != "0.3":
        raise HarnessError("Unsupported case catalogue/version")
    for name, expected in data["documents"].items():
        if name not in {"design.md", "test-cases.md"} or document_digest(FEATURE/name) != expected:
            raise HarnessError(f"Reviewed document changed: {name}; reconcile code/docs first")
    if [c["id"] for c in data["cases"]] != [f"MR-TC{i:02}" for i in range(1, 55)]:
        raise HarnessError("Catalogue must contain each MR-TC01..54 exactly once")
    for case in data["cases"]:
        if case["kind"] not in {"single", "repeat_registration", "correct_password",
                               "confirmation_presence"}:
            raise HarnessError(f"Unknown case kind: {case['id']}")
        for key in ("requires_existing", "requires_absent", "protect_existing"):
            case[key] = [e.replace(data["namespace"], namespace) for e in case[key]]
        for attempt in case["attempts"]:
            if attempt["expected"] not in {"ACCEPT", "REJECT"}:
                raise HarnessError("Expected outcome must come from reviewed case data")
            attempt["email"] = attempt["email"].replace(data["namespace"], namespace)
    return data


class ReadOnlyAccounts:
    """Read only the selected runtime DB. No importing backend/database.js."""
    COLUMNS = ("id", "name", "email", "role", "login_attempts", "locked_until",
               "shipping_address", "phone")

    def __init__(self, path):
        self.path = Path(path).resolve(strict=True)
        if self.path == (REPO / "backend/database.sqlite").resolve():
            raise HarnessError("Use the isolated runtime DB, not the tracked SUT database")

    def snapshot(self, emails):
        try:
            connection = sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True, timeout=3)
            try:
                connection.row_factory = sqlite3.Row
                connection.execute("PRAGMA query_only=ON")
                connection.execute("BEGIN")
                available = {r["name"] for r in connection.execute("PRAGMA table_info(users)")}
                if not {"id", "name", "email"} <= available:
                    raise HarnessError("Runtime users schema is not the documented SUT")
                columns = [name for name in self.COLUMNS if name in available]
                sql = ('SELECT ' + ','.join('"'+c+'"' for c in columns)
                       + ' FROM users WHERE email COLLATE BINARY = ? ORDER BY id')
                return {email: [dict(row) for row in connection.execute(sql, (email,))]
                        for email in sorted(set(emails))}
            finally:
                connection.close()
        except (sqlite3.Error, OSError) as error:
            raise HarnessError(f"Read-only account observation failed: {error}") from error

    def settled(self, emails, timeout):
        deadline = time.monotonic() + timeout
        previous = None
        unchanged_since = None
        while time.monotonic() < deadline:
            current = self.snapshot(emails)
            if current == previous:
                if unchanged_since is None:
                    unchanged_since = time.monotonic()
                if time.monotonic() - unchanged_since >= 0.4:
                    return current
            else:
                unchanged_since = None
            previous = current
            time.sleep(0.2)
        raise HarnessError("Account state did not settle; no reliable persistence verdict")


def check_connection(api_url):
    parsed = urlparse(api_url)
    if parsed.scheme != "http" or not parsed.netloc or parsed.query or parsed.fragment:
        raise HarnessError("Manifest mobile_api_url must be the configured local HTTP API URL")
    try:
        # A read-only availability check, never /register or /login.
        with urlopen(api_url.rstrip("/") + "/products", timeout=5) as response:
            if response.status != 200 or not isinstance(json.load(response), list):
                raise HarnessError("Backend product availability check failed")
    except (OSError, ValueError, URLError) as error:
        raise HarnessError(f"Backend not reachable: {error}") from error


def watched_emails(case):
    values = set(case["requires_existing"] + case["requires_absent"]
                 + case["protect_existing"])
    for attempt in case["attempts"]:
        raw = attempt["email"]
        # Observe variants to catch accidental lowercasing/storage of raw padding;
        # never send these observer variants to the native form.
        values.update((raw, raw.strip(), raw.strip().lower()))
    return values


def check_preconditions(case, before):
    for email in case["requires_existing"]:
        if not before.get(email):
            raise HarnessError(f"Fixture email must already exist: {email!r}")
    for email in case["requires_absent"]:
        if before.get(email):
            raise HarnessError(f"Case requires a new email, but it already exists: {email!r}")


def evaluate(attempt, before, after, observation):
    """Compare UI and observed persistence to the fixed documented oracle."""
    problems = []
    expected = attempt["expected"]
    canonical = attempt["email"].strip()
    if expected == "ACCEPT":
        old = before.get(canonical, [])
        new = after.get(canonical, [])
        if old:
            raise HarnessError("ACCEPT attempt no longer has the required new-email state")
        if len(new) != 1:
            problems.append(f"Expected exactly one new {canonical!r} account, observed {len(new)}")
        elif new[0]["name"] != attempt["name"] or new[0]["email"] != canonical:
            problems.append("Stored name/email differs from the documented input/normalization")
        for email, previous in before.items():
            if email != canonical and after.get(email, []) != previous:
                problems.append(f"Unexpected account change at watched identity {email!r}")
        if not observation["login"]:
            problems.append("Successful registration did not reach the native Login screen")
    else:
        if before != after:
            problems.append("Invalid/duplicate submission created or changed watched account data")
        if observation["success_signal"]:
            problems.append("Invalid submission reported registration success")
        if observation["login"]:
            problems.append("Invalid submission reached Login as if registration succeeded")
        if not observation["feedback"]:
            problems.append("No validation/failure feedback was observed")
    return problems


def execute_case(case, native, accounts, api_url, result, timeout):
    native.open_registration(restart=True)
    form = native.inspect_form()
    result["form"] = form
    if case["kind"] == "confirmation_presence":
        confirmation = form["fields"].get("confirmation")
        password = form["fields"].get("password")
        problems = []
        if not confirmation:
            problems.append("Required native Confirmation field is absent after full-form inspection")
        elif not confirmation["editable"]:
            problems.append("Confirmation exists but is not independently editable")
        elif password and password["bounds"] == confirmation["bounds"]:
            problems.append("Confirmation was bound to the same control as Password")
        native.capture("confirmation-presence")
        result["assertions"] = {"expected": "independent editable Confirmation field",
                                "problems": problems, "submissions": 0}
        if problems:
            raise CaseFailure("; ".join(problems))
        return
    if not {"name", "email", "password"} <= form["fields"].keys():
        raise HarnessError("Registration core fields could not be bound")
    if case["requires_confirmation"] and "confirmation" not in form["fields"]:
        raise HarnessError("C-guard: Confirmation missing; equality case cannot be performed natively")
    if "confirmation" not in form["fields"]:
        result["limitations"].append("Confirmation absent; this case does not exercise MR-R10")
    emails = watched_emails(case)
    before = accounts.snapshot(emails)
    check_preconditions(case, before)
    for step, attempt in enumerate(case["attempts"], 1):
        if step == 2 and case["kind"] == "repeat_registration":
            # TC13: navigate again, preserving account state between both submits.
            native.open_registration(restart=False)
            form = native.inspect_form()
        if attempt["fill"] == "password_only":
            # TC38: modify P/C on the current form, not N/E and not client/DB reset.
            for role in ("name", "email"):
                node = native.locate_field(role)
                if node.get("text", "") != attempt[role]:
                    raise HarnessError("TC38 password-only correction cannot preserve N/E precondition")
        check_connection(api_url)
        receipt_start = len(native.input_receipts)
        native.fill(attempt, form, password_only=attempt["fill"] == "password_only")
        before_step = accounts.snapshot(emails)
        observation = native.submit(step)  # Exactly one delivery per documented step.
        check_connection(api_url)
        after = accounts.settled(emails, timeout)
        problems = evaluate(attempt, before_step, after, observation)
        item = {"step": step, "input": deepcopy(attempt),
                "before": before_step, "after": after,
                "observation": observation,
                "input_receipts": native.input_receipts[receipt_start:],
                "problems": problems}
        result["attempts"].append(item)
        if problems:
            # Remaining sequence steps depend on this step's documented state.
            # Keep them not performed; do not repair DB or repeat a submit.
            result["unperformed_sequence_steps"] = len(case["attempts"]) - step
            raise CaseFailure("; ".join(problems))
        before = after
    if native.submission_count != len(case["attempts"]):
        raise HarnessError("Native submission count differs from the documented sequence")


def write_results(path, run):
    counts = {status: sum(c["status"] == status for c in run["cases"])
              for status in ("passed", "failed", "blocked", "not_run")}
    run["counts"] = {"designed": len(run["cases"]), **counts,
                     "executed": counts["passed"] + counts["failed"],
                     "not_executed": counts["blocked"] + counts["not_run"]}
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8", newline="\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Explicitly permit a real native run")
    parser.add_argument("--manifest", type=Path, required=True,
                        help="Existing services.json linking backend runtime DB and API URL")
    parser.add_argument("--sdk", type=Path, default=REPO.parent/".runtime/android-sdk")
    parser.add_argument("--device", default="emulator-5554")
    parser.add_argument("--expo-url", default="exp://10.0.2.2:8081")
    parser.add_argument("--package", default="host.exp.exponent")
    parser.add_argument("--namespace", default="t02r01")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("MR-%Y%m%dT%H%M%SZ"))
    parser.add_argument("--output", type=Path, default=FEATURE/"evidence")
    parser.add_argument("--case", nargs="+", dest="selected")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if not args.execute:
        parser.error("No execution requested. Add --execute only when a real run is authorized.")
    if (not re.fullmatch(r"[A-Za-z0-9_-]+", args.namespace)
            or not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id) or args.timeout <= 0):
        parser.error("Invalid namespace/run ID/timeout")
    try:
        catalogue = load_catalogue(args.namespace)
        manifest = read_json(args.manifest)
        # This path is required explicitly by the existing environment manifest.
        db_path = Path(manifest["backend_database"])
        if not db_path.is_absolute():
            raise HarnessError("Manifest backend_database must be an absolute runtime path")
        api_url = manifest["mobile_api_url"]
        accounts = ReadOnlyAccounts(db_path)
    except (HarnessError, KeyError, OSError) as error:
        parser.error(str(error))
    selected = set(args.selected or [case["id"] for case in catalogue["cases"]])
    if not selected or selected - {case["id"] for case in catalogue["cases"]}:
        parser.error("Unknown/empty TC selection")
    run_root = args.output.resolve()/args.run_id
    run_root.mkdir(parents=True, exist_ok=False)
    run = {"run_id": args.run_id, "started_at": utc_now(), "target": "native-android",
           "namespace": args.namespace, "selected": sorted(selected),
           "manifest": str(args.manifest.resolve()), "database": str(accounts.path),
           "api_url": api_url, "device": args.device, "expo_url": args.expo_url,
           "sut_source_commit_from_manifest": manifest.get("source_commit"),
           "documents": catalogue["documents"],
           "implementation_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in (FEATURE/"scripts").glob("*.py")},
           "cases": [{"id": c["id"], "status": "not_run", "technique": c["technique"],
                      "traceability": c["traceability"], "expected_text": c["expected_text"],
                      "document_line": c["document_line"], "attempts": [], "limitations": []}
                     for c in catalogue["cases"]]}
    result_path = run_root/"results.json"
    write_results(result_path, run)
    try:
        # Fail before the first native test if screenshot export is unavailable.
        import PIL.Image  # noqa: F401
        check_connection(api_url)
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                  capture_output=True, text=True, check=False)
        run["test_commit"] = revision.stdout.strip() if revision.returncode == 0 else None
        for case, result in zip(catalogue["cases"], run["cases"]):
            if case["id"] not in selected:
                continue
            result["started_at"] = utc_now()
            native = None
            try:
                native = NativeAndroid(args.sdk.resolve(), args.device, args.expo_url,
                                       args.package, run_root/case["id"], args.timeout)
                execute_case(case, native, accounts, api_url, result, args.timeout)
                result["status"] = "passed"
            except CaseFailure as error:
                result.update(status="failed", reason=str(error))
            except (HarnessError, OSError, ValueError) as error:
                result.update(status="blocked", reason=str(error))
            finally:
                if native is not None:
                    result["submissions"] = native.submission_count
                    try:
                        native.capture("case-ended")
                    except HarnessError as error:
                        result["limitations"].append(f"Final screenshot unavailable: {error}")
                        if result["status"] == "passed":
                            result.update(status="blocked", reason="Required JPG evidence unavailable")
                result["finished_at"] = utc_now()
                result["evidence_directory"] = case["id"]
                write_results(result_path, run)
    except (ImportError, HarnessError, OSError) as error:
        run["run_error"] = str(error)
        for result in run["cases"]:
            if result["id"] in selected and result["status"] == "not_run":
                result.update(status="blocked", reason=str(error))
    finally:
        run["finished_at"] = utc_now()
        write_results(result_path, run)
    print(json.dumps({"results": str(result_path), **run["counts"]}, ensure_ascii=False))
    return 1 if run["counts"]["failed"] or run["counts"]["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
