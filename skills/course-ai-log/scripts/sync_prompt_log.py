"""Merge source-backed messages into a readable assignment Prompt Log."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def anchor(record):
    return "msg-" + digest(record["source_id"] + "/" + record["id"])[:20]


def fence(text):
    longest = max((len(m.group()) for m in re.finditer(r"`+", text)), default=0)
    marker = "`" * max(3, longest + 1)
    return marker + "text\n" + text + ("" if text.endswith("\n") else "\n") + marker


def display_timezone(offset):
    if not isinstance(offset, str) or not re.fullmatch(r"[+-]\d{2}:\d{2}", offset):
        raise ValueError("utc_offset phải có dạng +07:00 hoặc -05:00.")
    hours, minutes = map(int, offset[1:].split(":"))
    if hours > 14 or minutes > 59 or (hours == 14 and minutes):
        raise ValueError("utc_offset phải nằm trong khoảng -14:00 đến +14:00.")
    delta = timedelta(hours=hours, minutes=minutes)
    return timezone(delta if offset[0] == "+" else -delta)


def displayed_time(value, offset="+07:00"):
    target = display_timezone(offset)
    if value is None:
        return "Chưa có thời gian từ nguồn"
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamp phải có múi giờ; không tự suy diễn giờ message.")
    return parsed.astimezone(target).strftime("%H:%M:%S %d/%m/%Y") + " (UTC" + offset + ")"


def ordered_messages(data):
    for source_id in data["sources"]:
        yield source_id, sorted(
            (r for r in data["messages"] if r["source_id"] == source_id),
            key=lambda r: r["sequence"],
        )


def ensure_prompt_ids(data):
    prompt_ids = data.setdefault("prompt_ids", {})
    used = set(prompt_ids.values())
    if len(used) != len(prompt_ids) or any(not re.fullmatch(r"P-\d{3,}", p) for p in used):
        raise ValueError("Mã prompt trong dữ liệu lưu không hợp lệ hoặc bị trùng.")
    next_number = max((int(p[2:]) for p in used), default=-1) + 1
    for _, records in ordered_messages(data):
        for record in records:
            if record["role"] == "user" and anchor(record) not in prompt_ids:
                prompt_ids[anchor(record)] = f"P-{next_number:03d}"
                next_number += 1


def render(data):
    config = data.get("document", {})
    assignment = config.get("assignment")
    offset = config.get("utc_offset", "+07:00")
    title = assignment + " Prompt Log" if assignment else "Prompt Log"
    lines = ["# " + title, ""]
    for source_id, records in ordered_messages(data):
        source = data["sources"][source_id]
        lines += ["Phạm vi: " + source["scope"], ""]
        source_note = source.get("display_note")
        if source["coverage"] == "partial":
            detail = source_note or source.get("coverage_note") or "Cần bổ sung các lượt còn thiếu."
            lines += ["> Log chưa đủ trong phạm vi này. " + detail, ""]
        elif source_note:
            lines += ["> " + source_note, ""]

        by_user_id = {
            r["id"]: data["prompt_ids"][anchor(r)]
            for r in records if r["role"] == "user"
        }
        nearest_prompt = None
        active_target = None
        output_started = False
        response_count = 0
        for record in records:
            lines += ['<a id="' + anchor(record) + '"></a>', ""]
            if record["role"] == "user":
                nearest_prompt = by_user_id[record["id"]]
                active_target = nearest_prompt
                output_started = False
                response_count = 0
                lines += ["## " + nearest_prompt, "",
                          "- Timestamp: " + displayed_time(record["timestamp"], offset),
                          "- Công cụ: " + record["tool"]]
                if record.get("model"):
                    lines += ["- Model: " + record["model"]]
                lines += ["", "### Prompt", ""]
            else:
                reply_to = record.get("reply_to")
                target = by_user_id.get(reply_to) if reply_to else nearest_prompt
                if target != active_target or target is None:
                    label = "Phản hồi bổ sung cho " + target if target else "Phản hồi thiếu prompt trong nguồn"
                    lines += ["## " + label, ""]
                    active_target = target
                    output_started = False
                    response_count = 0
                if not output_started:
                    lines += ["### Output", ""]
                    output_started = True
                response_count += 1
                lines += ["#### Phản hồi " + str(response_count) + " — "
                          + displayed_time(record["timestamp"], offset), "",
                          "- Công cụ: " + record["tool"]]
                if record.get("model"):
                    lines += ["- Model: " + record["model"]]
                lines += [""]
            if not record["verbatim"]:
                lines += ["> Nội dung đã được xử lý; không phải nguyên văn đầy đủ."]
                redaction_note = record.get("display_note") or record.get("note")
                if redaction_note:
                    lines[-1] += " " + redaction_note
                lines += [""]
            elif record.get("display_note"):
                lines += ["> " + record["display_note"], ""]
            lines += [fence(record["text"]), ""]
    return "\n".join(lines)


def document_config(incoming, data, assignment, utc_offset, log_name):
    previous = data.get("document", {})
    result = dict(previous)
    explicit = {"assignment": assignment, "utc_offset": utc_offset, "log_name": log_name}
    defaults = {"assignment": None, "utc_offset": "+07:00", "log_name": "prompt_log.md"}
    for key, default in defaults.items():
        from_input = incoming.get(key)
        from_cli = explicit[key]
        if from_input is not None and from_cli is not None and from_input != from_cli:
            raise ValueError("Input và tham số khác nhau ở trường " + key)
        proposed = from_cli if from_cli is not None else from_input
        if proposed is None:
            proposed = previous.get(key, default)
        if proposed is not None and (not isinstance(proposed, str) or not proposed.strip()):
            raise ValueError(key + " phải là chuỗi có nội dung.")
        if key == "assignment" and previous.get(key) and proposed != previous[key]:
            raise ValueError("Output-dir đã thuộc bài khác; dùng thư mục riêng cho mỗi bài.")
        if key == "log_name":
            if (not proposed.lower().endswith(".md") or "/" in proposed or "\\" in proposed
                    or any(c in proposed for c in '<>:"|?*\x00') or proposed in (".", "..")):
                raise ValueError("log_name phải là tên file Markdown nằm trong output-dir.")
            stored_name = previous.get(key, "prompt_log.md")
            if data.get("render_sha256") and proposed != stored_name:
                raise ValueError("Không đổi tên file log đang quản lý; bảo toàn file hiện hành trước.")
        result[key] = proposed
    display_timezone(result["utc_offset"])
    return result


def sync(input_path, output_dir, assignment=None, utc_offset=None, log_name=None):
    incoming = json.loads(Path(input_path).read_text(encoding="utf-8-sig"))
    for field in ("source_id", "scope", "source_kind", "tool"):
        if not isinstance(incoming.get(field), str) or not incoming[field].strip():
            raise ValueError("Thiếu trường nguồn: " + field)
    if incoming.get("coverage") not in ("partial", "complete_for_scope"):
        raise ValueError("coverage phải là partial hoặc complete_for_scope")
    if not isinstance(incoming.get("messages"), list) or not incoming["messages"]:
        raise ValueError("Cần ít nhất một message có nguồn.")
    output_dir = Path(output_dir)
    state_path = output_dir / "_data" / "interactions.json"
    data = {"schema_version": 2, "sources": {}, "messages": [], "render_sha256": None}
    if state_path.exists():
        data = json.loads(state_path.read_text(encoding="utf-8"))
        if data.get("schema_version") not in (1, 2):
            raise ValueError("Schema dữ liệu lưu chưa được hỗ trợ.")
    config = document_config(incoming, data, assignment, utc_offset, log_name)
    log_path = output_dir / config["log_name"]
    if log_path.exists():
        actual = log_path.read_bytes().decode("utf-8")
        expected = data.get("render_sha256")
        if expected is None or digest(actual) != expected:
            raise ValueError("File log đã được sửa tay hoặc không thuộc helper; dừng để bảo toàn.")
    source_id = incoming["source_id"]
    source = {}
    for key in ("scope", "source_kind", "coverage", "coverage_note", "display_note"):
        value = incoming.get(key, "")
        if not isinstance(value, str):
            raise ValueError(key + " của nguồn phải là chuỗi.")
        if value or key != "display_note":
            source[key] = value
    previous = data["sources"].get(source_id)
    if previous and (previous["scope"], previous["source_kind"]) != (source["scope"], source["source_kind"]):
        raise ValueError("Một source_id phải giữ cùng phạm vi và loại nguồn.")
    by_id = {(m["source_id"], m["id"]): m for m in data["messages"]}
    by_sequence = {(m["source_id"], m["sequence"]): m["id"] for m in data["messages"]}
    added = 0
    for msg in incoming["messages"]:
        if not isinstance(msg, dict):
            raise ValueError("Message phải là object.")
        if not isinstance(msg.get("id"), str) or not msg["id"].strip():
            raise ValueError("Message cần ID nguồn ổn định.")
        if type(msg.get("sequence")) is not int or msg["sequence"] < 1:
            raise ValueError("sequence phải là số nguyên dương theo thứ tự nguồn.")
        if msg.get("role") not in ("user", "assistant") or not isinstance(msg.get("text"), str):
            raise ValueError("Chỉ nhận role user/assistant và text nguyên văn.")
        if msg.get("timestamp") is not None and not isinstance(msg["timestamp"], str):
            raise ValueError("timestamp phải là ISO 8601 hoặc null.")
        displayed_time(msg.get("timestamp"), config["utc_offset"])
        if type(msg.get("verbatim", True)) is not bool:
            raise ValueError("verbatim phải là boolean.")
        if msg.get("verbatim", True) is False and not (msg.get("note") or msg.get("display_note")):
            raise ValueError("Nội dung đã ẩn/sửa phải có ghi chú.")
        record = {"source_id": source_id, "id": msg["id"], "sequence": msg["sequence"],
                  "role": msg["role"], "text": msg["text"], "timestamp": msg.get("timestamp"),
                  "tool": msg.get("tool") or incoming["tool"], "verbatim": msg.get("verbatim", True)}
        if not isinstance(record["tool"], str) or not record["tool"].strip():
            raise ValueError("Công cụ phải là chuỗi có nội dung.")
        for key in ("model", "channel", "reply_to", "note", "display_note"):
            if msg.get(key) is not None:
                if not isinstance(msg[key], str):
                    raise ValueError(key + " phải là chuỗi.")
                record[key] = msg[key]
        key = (source_id, record["id"])
        seq_key = (source_id, record["sequence"])
        if key in by_id:
            if by_id[key] != record:
                raise ValueError("ID đã có nhưng nội dung khác: " + record["id"])
            continue
        if seq_key in by_sequence:
            raise ValueError("Trùng sequence với message khác.")
        data["messages"].append(record)
        by_id[key] = record
        by_sequence[seq_key] = record["id"]
        added += 1
    data["schema_version"] = 2
    data["document"] = config
    data["sources"][source_id] = source
    ensure_prompt_ids(data)
    text = render(data)
    data["render_sha256"] = digest(text)
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(text, encoding="utf-8", newline="\n")
    state_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"added_messages": added, "total_messages": len(data["messages"]), "log": str(log_path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--assignment")
    parser.add_argument("--utc-offset")
    parser.add_argument("--log-name")
    args = parser.parse_args()
    try:
        print(json.dumps(sync(args.input, args.output_dir, args.assignment,
                              args.utc_offset, args.log_name), ensure_ascii=False))
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, "Không ghi log: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
