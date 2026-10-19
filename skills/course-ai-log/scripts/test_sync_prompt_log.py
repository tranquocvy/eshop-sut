"""Regression checks for content preservation and assignment log updates."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("sync_prompt_log.py")
SPEC = importlib.util.spec_from_file_location("course_log_sync", MODULE_PATH)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class PromptLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "ai"
        self.input_path = self.root / "input.json"
        self.payload = {
            "assignment": "HW03",
            "source_id": "source-one",
            "scope": "Thiết kế test theo yêu cầu bài mới",
            "source_kind": "synthetic-regression-fixture",
            "coverage": "complete_for_scope",
            "tool": "Fixture AI",
            "messages": [
                {"id": "u1", "sequence": 1, "role": "user", "text": "Giữ tiếng Việt và `code`.\n",
                 "timestamp": "2026-10-20T03:00:00Z", "note": "internal-source-location-123"},
                {"id": "a1", "sequence": 2, "role": "assistant", "text": "Tiến độ gốc\n```python\nprint('Việt')\n```\n",
                 "timestamp": "2026-10-20T03:01:00Z", "channel": "commentary", "reply_to": "u1"},
                {"id": "a2", "sequence": 3, "role": "assistant", "text": "Kết quả gốc 🌱",
                 "timestamp": "2026-10-20T03:02:00Z", "channel": "final", "reply_to": "u1"},
            ],
        }

    def run_sync(self, payload=None, **kwargs):
        payload = payload if payload is not None else self.payload
        self.input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return helper.sync(self.input_path, self.output, **kwargs)

    def state(self):
        return json.loads((self.output / "_data" / "interactions.json").read_text(encoding="utf-8"))

    def log(self):
        name = self.state()["document"]["log_name"]
        return (self.output / name).read_text(encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.output)): p.read_bytes()
                for p in self.output.rglob("*") if p.is_file()}

    def test_new_assignment_preserves_every_message_and_nested_code(self):
        result = self.run_sync()
        self.assertEqual(result["total_messages"], 3)
        state = self.state()
        self.assertEqual([m["text"] for m in state["messages"]],
                         [m["text"] for m in self.payload["messages"]])
        log = self.log()
        self.assertTrue(log.startswith("# HW03 Prompt Log"))
        self.assertNotIn("HW02", log)
        for message in self.payload["messages"]:
            self.assertIn(message["text"], log)
        self.assertIn("````text", log)
        self.assertNotIn("internal-source-location-123", log)
        self.assertEqual(state["messages"][0]["note"], "internal-source-location-123")

    def test_reimport_is_idempotent(self):
        self.run_sync()
        before = self.snapshot()
        self.assertEqual(self.run_sync()["added_messages"], 0)
        self.assertEqual(self.snapshot(), before)

    def test_incremental_sources_keep_prompt_labels_and_message_order(self):
        self.run_sync()
        first_ids = dict(self.state()["prompt_ids"])
        second = copy.deepcopy(self.payload)
        second["source_id"] = "source-two"
        second["messages"] = [{"id": "u2", "sequence": 1, "role": "user", "text": "Yêu cầu sửa",
                               "timestamp": None}]
        self.run_sync(second)
        self.payload["messages"].append({"id": "u3", "sequence": 4, "role": "user",
                                         "text": "Bổ sung lượt cũ", "timestamp": None})
        self.run_sync()
        state = self.state()
        for key, value in first_ids.items():
            self.assertEqual(state["prompt_ids"][key], value)
        self.assertEqual(len(set(state["prompt_ids"].values())), 3)
        self.assertLess(self.log().index("Tiến độ gốc"), self.log().index("Kết quả gốc"))

    def test_late_reply_does_not_pair_with_wrong_prompt_or_reorder(self):
        self.payload["messages"] += [
            {"id": "u2", "sequence": 4, "role": "user", "text": "PROMPT TWO", "timestamp": None},
            {"id": "a3", "sequence": 5, "role": "assistant", "text": "LATE FIRST REPLY",
             "timestamp": None, "reply_to": "u1"},
        ]
        self.run_sync()
        log = self.log()
        self.assertIn("Phản hồi bổ sung cho P-000", log)
        self.assertLess(log.index("PROMPT TWO"), log.index("LATE FIRST REPLY"))

    def test_missing_prompt_is_explicit_without_inventing_one(self):
        self.payload["messages"][-1]["reply_to"] = "outside-source"
        self.run_sync()
        self.assertIn("Phản hồi thiếu prompt trong nguồn", self.log())
        self.assertEqual(len(self.state()["prompt_ids"]), 1)

    def test_redaction_is_separate_from_missing_turns(self):
        self.payload["messages"][-1].update(verbatim=False, display_note="Ẩn đường dẫn riêng tư.")
        self.run_sync()
        self.assertIn("Ẩn đường dẫn riêng tư", self.log())
        self.assertNotIn("Log chưa đủ", self.log())
        self.assertFalse(self.state()["messages"][-1]["verbatim"])

    def test_partial_scope_and_unknown_time_are_not_fabricated(self):
        self.payload.update(coverage="partial", display_note="Thiếu phản hồi cuối.")
        self.payload["messages"][0]["timestamp"] = None
        self.run_sync()
        self.assertIn("Thiếu phản hồi cuối", self.log())
        self.assertIn("Chưa có thời gian từ nguồn", self.log())
        self.assertIsNone(self.state()["messages"][0]["timestamp"])

    def test_custom_filename_timezone_and_source_timestamp(self):
        self.run_sync(log_name="student_HW03_PromptLog.md", utc_offset="-05:00")
        self.assertIn("22:00:00 19/10/2026 (UTC-05:00)", self.log())
        self.assertEqual(self.state()["messages"][0]["timestamp"], "2026-10-20T03:00:00Z")
        self.assertFalse((self.output / "prompt_log.md").exists())
        self.run_sync()

    def test_manual_edit_is_preserved(self):
        self.run_sync()
        path = self.output / "prompt_log.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nSV sửa tay.\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_sync()
        self.assertEqual(before, self.snapshot())

    def test_unmanaged_log_is_not_overwritten(self):
        self.output.mkdir()
        (self.output / "prompt_log.md").write_text("Log SV đã viết", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            self.run_sync()
        self.assertEqual(before, self.snapshot())

    def test_assignment_mix_is_rejected_without_writes(self):
        self.run_sync()
        before = self.snapshot()
        other = copy.deepcopy(self.payload)
        other["assignment"] = "HW04"
        with self.assertRaises(ValueError):
            self.run_sync(other)
        self.assertEqual(before, self.snapshot())

    def test_conflicting_records_or_source_do_not_write(self):
        self.run_sync()
        before = self.snapshot()
        variants = []
        changed_text = copy.deepcopy(self.payload)
        changed_text["messages"][0]["text"] = "Lời khác"
        variants.append(changed_text)
        changed_id = copy.deepcopy(self.payload)
        changed_id["messages"][0]["id"] = "different-id-same-sequence"
        variants.append(changed_id)
        changed_scope = copy.deepcopy(self.payload)
        changed_scope["scope"] = "Phạm vi khác"
        variants.append(changed_scope)
        invalid_tail = copy.deepcopy(self.payload)
        invalid_tail["messages"] += [
            {"id": "u2", "sequence": 4, "role": "user", "text": "Chưa được ghi", "timestamp": None},
            {"id": "bad", "sequence": 0, "role": "user", "text": "Bad", "timestamp": None},
        ]
        variants.append(invalid_tail)
        for variant in variants:
            with self.subTest(variant=variant):
                with self.assertRaises(ValueError):
                    self.run_sync(variant)
                self.assertEqual(before, self.snapshot())

    def test_invalid_inputs_reject_before_creating_output(self):
        variants = []
        for field, value in (("timestamp", "2026-10-20T10:00:00"), ("sequence", True),
                             ("role", "system"), ("text", None), ("verbatim", "true")):
            bad = copy.deepcopy(self.payload)
            bad["messages"][0][field] = value
            variants.append(bad)
        for field, value in (("utc_offset", "+14:01"), ("log_name", "../escape.md"),
                             ("coverage", "guess")):
            bad = copy.deepcopy(self.payload)
            bad[field] = value
            variants.append(bad)
        for bad in variants:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.run_sync(bad)
                self.assertFalse(self.output.exists())

    def test_schema_one_migration_keeps_records_and_old_anchors(self):
        self.run_sync()
        state = self.state()
        original_records = copy.deepcopy(state["messages"])
        old_anchors = [helper.anchor(r) for r in original_records]
        state["schema_version"] = 1
        del state["document"]
        del state["prompt_ids"]
        old_log = "# Nhật ký cũ\nNội dung do helper v1 quản lý.\n"
        state["render_sha256"] = helper.digest(old_log)
        (self.output / "prompt_log.md").write_text(old_log, encoding="utf-8", newline="\n")
        (self.output / "_data" / "interactions.json").write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual(self.run_sync()["added_messages"], 0)
        self.assertEqual(self.state()["schema_version"], 2)
        self.assertEqual(self.state()["messages"], original_records)
        for old_anchor in old_anchors:
            self.assertIn(old_anchor, self.log())

    def test_command_line_runs_same_helper(self):
        self.input_path.write_text(json.dumps(self.payload), encoding="utf-8")
        completed = subprocess.run([sys.executable, str(MODULE_PATH), "--input", str(self.input_path),
                                    "--output-dir", str(self.output)], capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("utf-8", errors="replace"))
        self.assertEqual(self.state()["document"]["assignment"], "HW03")
        self.assertEqual(len(self.state()["messages"]), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
