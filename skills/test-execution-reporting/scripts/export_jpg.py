"""Export verified JPEG; optionally remove a task-generated temporary PNG."""
import argparse
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path


def export_jpg(input_path, output_path, *, remove_source=False):
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError("Cần Python có Pillow để chuyển ảnh; ưu tiên runtime sẵn có.") from exc

    requested_source = Path(input_path).expanduser()
    if remove_source and requested_source.is_symlink():
        raise ValueError("Không xóa nguồn qua symlink; chỉ dùng PNG tạm của task.")
    source = requested_source.resolve(strict=True)
    requested_output = Path(output_path).expanduser().absolute()
    if requested_output.is_symlink():
        raise ValueError("Không ghi đè symlink ở đường dẫn ảnh đích.")
    destination = requested_output.resolve()
    if source == destination:
        raise ValueError("Ảnh nguồn và ảnh đích phải khác nhau để xác minh trước khi dọn nguồn.")
    if destination.suffix.lower() not in (".jpg", ".jpeg"):
        raise ValueError("Ảnh JPEG đích cần phần mở rộng .jpg hoặc .jpeg.")
    if destination.exists():
        raise ValueError("Ảnh đích đã tồn tại; dùng tên/run mới, không ghi đè evidence.")

    original_bytes = source.read_bytes()
    with Image.open(BytesIO(original_bytes)) as original:
        if getattr(original, "n_frames", 1) != 1:
            raise ValueError("Chỉ nhận ảnh tĩnh; không bỏ các frame của evidence động.")
        source_format = original.format
        if remove_source and (source_format != "PNG" or source.suffix.lower() != ".png"):
            raise ValueError("--remove-source chỉ hỗ trợ PNG tạm; các ảnh khác được giữ nguyên.")
        source_size = original.size
        orientation = original.getexif().get(274, 1)
        oriented = ImageOps.exif_transpose(original)
        rgba = oriented.convert("RGBA")
        rgb = Image.new("RGB", rgba.size, "white")
        rgb.paste(rgba, mask=rgba.getchannel("A"))
        output_size = rgb.size
        encoded = BytesIO()
        rgb.save(encoded, format="JPEG", quality=95, subsampling=0, optimize=True)
    jpeg_bytes = encoded.getvalue()
    with Image.open(BytesIO(jpeg_bytes)) as verified:
        verified.load()
        if verified.format != "JPEG" or verified.size != output_size:
            raise ValueError("Ảnh xuất không giải mã đúng JPEG/kích thước dự kiến.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as output:
        output.write(jpeg_bytes)
    # Verify the actual file on disk before deleting any temporary source.
    with Image.open(destination) as saved:
        saved.load()
        if saved.format != "JPEG" or saved.size != output_size:
            raise ValueError("JPG trên đĩa không hợp lệ; giữ nguyên ảnh nguồn.")
    if remove_source:
        if source.read_bytes() != original_bytes:
            raise ValueError("Ảnh nguồn đã thay đổi trong khi xuất; giữ nguồn, không xóa.")
        source.unlink()
    return {
        "source": str(source),
        "output": str(destination),
        "source_format": source_format,
        "output_format": "JPEG",
        "source_dimensions": list(source_size),
        "output_dimensions": list(output_size),
        "exif_orientation_applied": orientation in (2, 3, 4, 5, 6, 7, 8),
        "source_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "source_retained": not remove_source,
        "output_sha256": hashlib.sha256(jpeg_bytes).hexdigest(),
        "converted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--remove-source", action="store_true",
                        help="Xóa PNG tạm do task tạo sau khi xác minh JPG; mặc định giữ nguồn.")
    args = parser.parse_args()
    try:
        print(json.dumps(export_jpg(args.input, args.output, remove_source=args.remove_source), ensure_ascii=False))
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, "Không xuất JPG: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
