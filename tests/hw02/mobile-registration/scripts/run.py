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
    native.open_registration(restart=False)
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
        result["pending_attempt"] = {"step": step, "input": deepcopy(attempt),
                                     "at": utc_now(), "before": before_step,
                                     "input_receipts": native.input_receipts[receipt_start:]}
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
        result.pop("pending_attempt", None)
        if problems:
            # Remaining sequence steps depend on this step's documented state.
            # Keep them not performed; do not repair DB or repeat a submit.
            result["unperformed_sequence_steps"] = len(case["attempts"]) - step
            raise CaseFailure("; ".join(problems))
        before = after
    if native.submission_count != len(case["attempts"]):
        raise HarnessError("Native submission count differs from the documented sequence")


def compact_attempt(attempt):
    observations = []
    for email, before in attempt["before"].items():
        after = attempt["after"][email]
        old_ids = {row["id"] for row in before}
        observations.append({"email": email, "count_before": len(before), "count_after": len(after),
                             "existing_rows_unchanged": all(row in after for row in before),
                             "new_accounts": [{k: row[k] for k in ("id", "name", "email")}
                                              for row in after if row["id"] not in old_ids]})
    return {"step": attempt["step"], "input": {k: v for k, v in attempt["input"].items() if k != "fill"},
            "ui": attempt["observation"], "accounts": observations,
            "assertion_failures": attempt["problems"],
            "input_verification": [{"field": r["field"], "readback": r["readback"]}
                                   for r in attempt["input_receipts"]]}


def actual_text(result):
    if result.get("assertions"):
        return ("Full-form inspection: " + "; ".join(result["assertions"]["problems"])
                if result["assertions"]["problems"] else "Independent editable Confirmation field observed.")
    parts = []
    for step in result["steps"]:
        changes = [f'{a["count_before"]}→{a["count_after"]}' for a in step["accounts"]
                   if a["count_before"] != a["count_after"]]
        ui = step["ui"]
        message = "báo thành công" if ui["success_signal"] else (
            "có phản hồi từ chối" if ui["feedback"] else "không feedback")
        parts.append(f'bước {step["step"]}: tài khoản ' + ("/".join(changes) if changes else "không đổi")
                     + "; " + message + "; " + ("Đăng nhập" if ui["login"] else "form Đăng ký"))
    if result["status"] == "blocked":
        parts.append(result["reason"])
    return "; ".join(parts)


def write_shared(path, shared):
    selected = {}
    run_types = {r["id"]: r.get("purpose") for r in shared["runs"]}
    for case in shared["cases"]:
        selected[case["id"]] = next(r for r in reversed(case["results"])
                                     if run_types.get(r["run_id"]) != "harness_probe")
    statuses = [r["status"] for r in selected.values()]
    counts = {key: statuses.count(key) for key in ("passed", "failed", "blocked", "not_run")}
    executed = counts["passed"] + counts["failed"]
    shared["summary"] = {"designed": len(statuses), **counts, "executed": executed,
                         "not_executed": counts["blocked"] + counts["not_run"],
                         "completed_status_entries": len(statuses) - counts["not_run"],
                         "interrupted_cases": [k for k, r in selected.items() if r.get("interrupted")],
                         "never_started": sum(r["status"] == "not_run" and not r.get("started_at")
                                              for r in selected.values()),
                         "pass_rate_executed_percent": round(100 * counts["passed"] / executed, 2) if executed else 0}
    shared["selected_results"] = {k: r["run_id"] for k, r in selected.items()}
    shared["counting_policy"] = ("Latest recorded main/resume result per unique TC, selected_results maps TC to run. "
                                 "Prior attempts/probes remain in history. executed=passed+failed; "
                                 "blocked/not_run are not executed. Interrupted submissions are not replayed.")
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(shared, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sdk", type=Path, default=REPO.parent/".runtime/android-sdk")
    parser.add_argument("--device", default="emulator-5554")
    parser.add_argument("--expo-url", default="exp://10.0.2.2:8083")
    parser.add_argument("--package", default="host.exp.exponent")
    parser.add_argument("--namespace", default="t02r01")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("MR-%Y%m%dT%H%M%SZ"))
    parser.add_argument("--case", nargs="+", dest="selected")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if not args.execute:
        parser.error("No execution requested. Add --execute only when a real run is authorized.")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.namespace) or not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        parser.error("Invalid namespace/run ID")
    catalogue = load_catalogue(args.namespace)
    manifest = read_json(args.manifest)
    path = FEATURE / "results.json"
    shared = read_json(path)
    if shared.get("schema_version") != 2 or shared.get("design_version") != catalogue["design_version"]:
        parser.error("A compatible shared results.json is required before resuming")
    if any(r["id"] == args.run_id for r in shared["runs"]):
        parser.error("Run ID already exists; preserve history")
    if [c["id"] for c in shared["cases"]] != [c["id"] for c in catalogue["cases"]]:
        parser.error("Shared results and catalogue disagree")
    if any(c["expected"] != d["expected_text"] for c, d in zip(shared["cases"], catalogue["cases"])):
        parser.error("Expected outcomes differ from the reviewed catalogue")
    accounts = ReadOnlyAccounts(manifest["backend_database"])
    api_url = manifest["mobile_api_url"]
    selected = set(args.selected or [c["id"] for c in shared["cases"]
                                    if c["results"][-1]["status"] in {"blocked", "not_run"}])
    if not selected or selected - {c["id"] for c in catalogue["cases"]}:
        parser.error("Unknown/empty TC selection")
    check_connection(api_url)
    # Record safe read-only preflight for interrupted TC29 before touching its form.
    before_resume = accounts.snapshot(["mr." + args.namespace + ".tc29@example.com",
                                      "mr." + args.namespace + ".tc26@example.com", "TEST@eshop.com"])
    environment = deepcopy(shared["runs"][0]["environment"])
    environment.pop("harness_diff", None)
    environment["prior_harness_revision"] = "MR-RUN-01; current implementation hashes recorded in this run"
    environment["harness_changes"] = ("Reuse native session; --no-idle layout plus explicit readiness predicates; "
                                       "dismiss IME if inline validation hides the focused field; "
                                       "observe visible validation even when unchanged from previous attempt; "
                                       "one shared result file; no layout dumps or trace files; "
                                       "JPG only for new failure groups. No business/expected changes.")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True)
    run = {"id": args.run_id, "purpose": "resume", "state": "running", "started_at": utc_now(),
           "namespace": args.namespace, "selected": sorted(selected), "source_commit": revision.stdout.strip(),
           "sources": {"documents": catalogue["documents"], "design_version": catalogue["design_version"],
                       "implementation_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                                  for p in (FEATURE/"scripts").glob("*.py")}},
           "environment": environment, "executor": "OpenAI Codex via Android CLI/adb; SQLite observations read-only",
           "resume_preflight": {email: len(rows) for email, rows in before_resume.items()}}
    shared["runs"].append(run)
    shared["selected_run_id"] = args.run_id
    write_shared(path, shared)
    native = NativeAndroid(args.sdk.resolve(), args.device, args.expo_url, args.package, FEATURE/"images", args.timeout)
    consecutive_harness_errors = 0
    failure_groups = {}
    try:
        for case, entry in zip(catalogue["cases"], shared["cases"]):
            if case["id"] not in selected:
                continue
            native.begin_case()
            result = {"run_id": args.run_id, "started_at": utc_now(), "status": "not_run",
                      "attempts": [], "limitations": []}
            entry["results"].append(result)
            write_shared(path, shared)
            try:
                execute_case(case, native, accounts, api_url, result, args.timeout)
                result["status"] = "passed"
            except CaseFailure as error:
                result.update(status="failed", reason=str(error))
            except (HarnessError, OSError, ValueError) as error:
                result.update(status="blocked", reason=str(error))
            except KeyboardInterrupt:
                result.update(status="not_run", interrupted=True,
                              reason="Interrupted; inspect native screen and account state before resuming")
                raise
            finally:
                result["submissions"] = native.submission_count
                result["steps"] = [compact_attempt(a) for a in result.pop("attempts")]
                if result.get("pending_attempt"):
                    pending = result.pop("pending_attempt")
                    result["incomplete_attempt"] = {"step": pending["step"], "input": pending["input"],
                                                    "at": pending["at"], "submission_count": native.submission_count,
                                                    "readbacks": [{"field": r["field"], "readback": r["readback"]}
                                                                  for r in pending["input_receipts"]]}
                result["finished_at"] = utc_now()
                result["actual"] = actual_text(result)
                if result["status"] == "failed":
                    # Share an image only when the oracle group AND assertion failures match.
                    rule_group = re.match(r"R\d+", case["traceability"]).group(0)
                    problems = [p for step in result["steps"] for p in step["assertion_failures"]]
                    signature = (rule_group, tuple(re.sub(r"'[^']*'", "<identity>", p) for p in problems),
                                 tuple(result.get("assertions", {}).get("problems", [])))
                    if signature in failure_groups:
                        result["images"] = failure_groups[signature]
                        result["shared_image_note"] = "Representative image from same rule/assertion failure group; own observations retained."
                    else:
                        try:
                            result["images"] = native.save_failure_images(args.run_id + "-" + case["id"])
                            failure_groups[signature] = result["images"]
                            shared["images"].extend({**img, "tc": case["id"], "run_id": args.run_id}
                                                    for img in result["images"])
                        except HarnessError as error:
                            result["limitations"].append("Failure image unavailable: " + str(error))
                write_shared(path, shared)
                print(json.dumps({"case": case["id"], "status": result["status"],
                                  "actual": result["actual"]}, ensure_ascii=False), flush=True)
            if result["status"] == "blocked":
                if result.get("reason", "").startswith("C-guard:"):
                    # Known product-schema dependency, not a repeated transport failure.
                    consecutive_harness_errors = 0
                    continue
                consecutive_harness_errors += 1
                if result["submissions"] or consecutive_harness_errors >= 2:
                    run["stop_reason"] = "Uncertain submitted state or repeated harness error; no further automatic replay."
                    break
            else:
                consecutive_harness_errors = 0
        run["state"] = "stopped" if run.get("stop_reason") else "finished"
    except KeyboardInterrupt:
        run.update(state="interrupted", stop_reason="User interrupted; inspect screen/account state before any resume")
        raise
    finally:
        run["finished_at"] = utc_now()
        write_shared(path, shared)
        native.scratch.cleanup()
    print(json.dumps(shared["summary"], ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
