import os
import tempfile

from src import scanner


def test_image_ocr_monkeypatched(monkeypatch):
    # Create a temporary image file path (no real image needed for this monkeypatch)
    with tempfile.TemporaryDirectory() as tmp:
        img_path = os.path.join(tmp, "photo.jpg")
        # write a dummy file so the path exists
        with open(img_path, "wb") as f:
            f.write(b"\x00\x01")

        # Monkeypatch the OCR function to avoid requiring tesseract binary
        monkeypatch.setattr(scanner, "extract_text_from_image", lambda p, max_chars=2000: "This is a photo of a beach")

        txt = scanner.extract_text_from_file(img_path)
        assert txt is not None
        assert "beach" in txt
