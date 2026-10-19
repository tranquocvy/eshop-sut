"""Image conversion regression tests; fixtures are synthetic, not SUT evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

from export_jpg import export_jpg


class ExportJpgTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="jpg-fixture-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "synthetic-fixture.png"
        image = Image.new("RGBA", (320, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle((10, 10, 310, 90), fill=(240, 240, 240, 255))
        draw.text((20, 40), "SYNTHETIC CONVERSION FIXTURE", fill=(0, 0, 0, 255))
        image.save(self.source)
        self.destination = self.root / "export/fixture.jpg"

    def test_png_becomes_decodable_jpeg_and_preserves_source(self):
        before = self.source.read_bytes()
        metadata = export_jpg(self.source, self.destination)
        self.assertEqual(before, self.source.read_bytes())
        self.assertEqual(metadata["source_format"], "PNG")
        self.assertEqual(metadata["output_format"], "JPEG")
        self.assertEqual(metadata["source_sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(metadata["output_sha256"], hashlib.sha256(self.destination.read_bytes()).hexdigest())
        with Image.open(self.destination) as result:
            result.load()
            self.assertEqual(result.format, "JPEG")
            self.assertEqual(result.size, (320, 100))
            self.assertTrue(all(channel >= 245 for channel in result.getpixel((0, 0))))
        self.assertNotIn("captured_at", metadata)
        self.assertIn("converted_at", metadata)
        self.assertTrue(metadata["source_retained"])

    def test_temporary_png_can_be_removed_after_verified_export(self):
        metadata = export_jpg(self.source, self.destination, remove_source=True)
        self.assertFalse(self.source.exists())
        self.assertFalse(metadata["source_retained"])
        with Image.open(self.destination) as saved:
            saved.load()
            self.assertEqual(saved.format, "JPEG")
            self.assertEqual(saved.size, (320, 100))

    def test_remove_source_refuses_non_png_and_keeps_it(self):
        source = self.root / "provided.jpg"
        Image.new("RGB", (80, 40), "blue").save(source, format="JPEG")
        before = source.read_bytes()
        with self.assertRaises(ValueError):
            export_jpg(source, self.destination, remove_source=True)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse(self.destination.exists())

    def test_existing_jpeg_input_is_supported_without_changing_original(self):
        source = self.root / "source.jpg"
        Image.new("RGB", (80, 40), "blue").save(source, format="JPEG")
        before = source.read_bytes()
        metadata = export_jpg(source, self.destination)
        self.assertEqual(metadata["source_format"], "JPEG")
        self.assertEqual(source.read_bytes(), before)

    def test_existing_destination_is_preserved(self):
        self.destination.parent.mkdir()
        self.destination.write_bytes(b"Existing evidence must stay unchanged")
        before = self.destination.read_bytes()
        with self.assertRaises(ValueError):
            export_jpg(self.source, self.destination, remove_source=True)
        self.assertEqual(self.destination.read_bytes(), before)
        self.assertTrue(self.source.exists())

    def test_same_source_and_destination_are_rejected(self):
        before = self.source.read_bytes()
        with self.assertRaises(ValueError):
            export_jpg(self.source, self.source)
        self.assertEqual(self.source.read_bytes(), before)

    def test_invalid_image_or_wrong_extension_produces_no_output(self):
        invalid = self.root / "not-an-image.png"
        invalid.write_text("Synthetic invalid data", encoding="utf-8")
        with self.assertRaises(OSError):
            export_jpg(invalid, self.destination)
        self.assertFalse(self.destination.exists())
        wrong_output = self.root / "wrong.png"
        with self.assertRaises(ValueError):
            export_jpg(self.source, wrong_output)
        self.assertFalse(wrong_output.exists())

    def test_exif_display_orientation_is_respected_without_resizing(self):
        source = self.root / "rotated.jpg"
        image = Image.new("RGB", (80, 40), "green")
        exif = image.getexif()
        exif[274] = 6
        image.save(source, format="JPEG", exif=exif)
        metadata = export_jpg(source, self.destination)
        self.assertEqual(metadata["source_dimensions"], [80, 40])
        self.assertEqual(metadata["output_dimensions"], [40, 80])
        self.assertTrue(metadata["exif_orientation_applied"])

    def test_animation_is_not_silently_reduced_to_one_frame(self):
        source = self.root / "animated.gif"
        Image.new("RGB", (10, 10), "red").save(source, save_all=True,
            append_images=[Image.new("RGB", (10, 10), "blue")], duration=100, loop=0)
        with self.assertRaises(ValueError):
            export_jpg(source, self.destination)
        self.assertFalse(self.destination.exists())

    def test_command_line_exports_verified_file_and_metadata(self):
        completed = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("export_jpg.py")),
            "--input", str(self.source), "--output", str(self.destination), "--remove-source"], capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("utf-8", errors="replace"))
        metadata = json.loads(completed.stdout)
        self.assertEqual(metadata["output_format"], "JPEG")
        self.assertTrue(self.destination.is_file())
        self.assertFalse(self.source.exists())
        self.assertFalse(metadata["source_retained"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
