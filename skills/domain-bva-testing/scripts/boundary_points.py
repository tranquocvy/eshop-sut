"""Calculate ISTQB-style items for explicitly supplied adjacent discrete partitions."""
import argparse
from decimal import Decimal, InvalidOperation, localcontext
import json
from pathlib import Path


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError(label + ": dùng chuỗi thập phân hoặc số nguyên, không dùng float.")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(label + ": giá trị thập phân không hợp lệ.") from exc
    if not result.is_finite():
        raise ValueError(label + ": không nhận NaN/Infinity.")
    return result


def formatted(value):
    return format(value, "f")


def derive(config, variant):
    if not isinstance(config, dict):
        raise ValueError("Input phải là JSON object.")
    if variant not in ("istqb-2", "istqb-3"):
        raise ValueError("Chỉ hỗ trợ istqb-2 hoặc istqb-3; không tự suy ra biến thể bài giảng.")
    for key in ("variable", "unit"):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError("Thiếu " + key)
    step = number(config.get("step"), "step")
    if step <= 0:
        raise ValueError("step phải dương.")
    origin = number(config.get("origin", "0"), "origin")
    minimum = None if config.get("min_value") is None else number(config["min_value"], "min_value")
    maximum = None if config.get("max_value") is None else number(config["max_value"], "max_value")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("min_value không được lớn hơn max_value.")
    edges = config.get("edges")
    if not isinstance(edges, list) or not edges:
        raise ValueError("Cần ít nhất một cặp biên được analyst xác định.")
    ids, global_values, output = set(), set(), []
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("Mỗi edge phải là object.")
        for key in ("id", "left_partition", "right_partition", "source_ref"):
            if not isinstance(edge.get(key), str) or not edge[key].strip():
                raise ValueError("Edge thiếu " + key)
        if edge["id"] in ids:
            raise ValueError("Trùng edge ID: " + edge["id"])
        ids.add(edge["id"])
        if edge["left_partition"] == edge["right_partition"]:
            raise ValueError("Cặp biên phải có hai partition khác nhau.")
        left, right = number(edge.get("left"), "left"), number(edge.get("right"), "right")
        values = [step, origin, left, right] + [v for v in (minimum, maximum) if v is not None]
        # Keep arithmetic exact for the finite values supplied, including large integers.
        precision = max(50, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in values) + 10)
        with localcontext() as ctx:
            ctx.prec = precision
            if right - left != step:
                raise ValueError("left/right phải liền kề theo step: " + edge["id"])
            for value in (left, right):
                if (value - origin) % step != 0:
                    raise ValueError("Điểm không nằm trên lattice origin + k*step.")
                if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
                    raise ValueError("Boundary value nằm ngoài giới hạn biểu diễn.")
            selected = {}
            for side, boundary in (("left", left), ("right", right)):
                offsets = (0,) if variant == "istqb-2" else (-1, 0, 1)
                for offset in offsets:
                    value = boundary + offset * step
                    selected.setdefault(value, []).append({"side": side, "offset": offset})
            items, excluded = [], []
            for value in sorted(selected):
                item = {"value": formatted(value), "derived_from": selected[value]}
                if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
                    item["reason"] = "Ngoài giới hạn biểu diễn đã khai báo; không tự gọi là test nhập được."
                    excluded.append(item)
                else:
                    item["id"] = edge["id"] + "-V" + str(len(items) + 1)
                    items.append(item)
                    global_values.add(value)
            output.append({"id": edge["id"], "source_ref": edge["source_ref"],
                           "left_partition": edge["left_partition"], "right_partition": edge["right_partition"],
                           "boundary_values": [formatted(left), formatted(right)],
                           "coverage_items": items, "unrepresentable_neighbors": excluded})
    return {"variable": config["variable"], "unit": config["unit"], "variant": variant,
            "step": formatted(step), "origin": formatted(origin), "scope_note": config.get("scope_note", ""),
            "scope_limit": "Chỉ tính điểm từ các edge đầu vào; chưa xác minh inventory, oracle, bài giảng hoặc execution.",
            "edges": output, "unique_values": [formatted(v) for v in sorted(global_values)]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--variant", required=True, choices=("istqb-2", "istqb-3"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        config = json.loads(args.input.read_text(encoding="utf-8-sig"), parse_float=Decimal)
        result = derive(config, args.variant)
        text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8", newline="\n")
        else:
            print(text, end="")
    except (ValueError, InvalidOperation, KeyError, OSError) as exc:
        parser.exit(1, "Không sinh điểm biên: " + str(exc) + "\n")
