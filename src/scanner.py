import os
from typing import Optional
from pypdf import PdfReader

# Optional image/OCR support
try:
    from PIL import Image
    import pytesseract
    _OCR_AVAILABLE = True
except Exception:
    Image = None  # type: ignore
    pytesseract = None  # type: ignore
    _OCR_AVAILABLE = False


def extract_text_from_file(path: str, max_chars: int = 5000) -> Optional[str]:
    """Extracts a text sample from a file based on its extension.

    Supports simple text-based formats and PDFs. Returns None for binary/unsupported files.
    """
    if not os.path.isfile(path):
        return None

    _, ext = os.path.splitext(path.lower())

    try:
        if ext in ('.txt', '.md', '.py', '.json', '.csv', '.rst'):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read(max_chars)
                return data

        if ext == '.pdf':
            try:
                reader = PdfReader(path)
                text = []
                for p in reader.pages[:3]:
                    page_text = p.extract_text() or ""
                    text.append(page_text)
                    if sum(len(t) for t in text) >= max_chars:
                        break
                joined = "\n".join(text)
                return joined[:max_chars]
            except Exception:
                return None

        # Image files: try OCR if available
        if ext in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'):
            if not _OCR_AVAILABLE:
                return None
            try:
                return extract_text_from_image(path, max_chars=max_chars)
            except Exception:
                return None

    except Exception:
        return None

    return None


def sample_texts_in_folder(folder_path: str, max_files: int = 8, chars_per_file: int = 2000):
    """Walk a folder and return a list of extracted text samples from files.

    The function prefers text-like files and returns up to `max_files` samples.
    """
    samples = []
    if not os.path.isdir(folder_path):
        return samples

    for root, _, files in os.walk(folder_path):
        for fname in files:
            if len(samples) >= max_files:
                break
            path = os.path.join(root, fname)
            txt = extract_text_from_file(path, max_chars=chars_per_file)
            if txt and txt.strip():
                header = f"--- {os.path.relpath(path, folder_path)} ---\n"
                samples.append(header + txt)
        if len(samples) >= max_files:
            break

    return samples


def extract_text_from_image(path: str, max_chars: int = 2000) -> Optional[str]:
    """Use pytesseract to OCR an image and return extracted text (truncated)."""
    if not _OCR_AVAILABLE:
        return None
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        if not text:
            return None
        return text[:max_chars]
    except Exception:
        return None


def extract_exif(path: str) -> dict:
    """Return basic EXIF metadata for an image (empty dict if not available)."""
    if Image is None:
        return {}
    try:
        img = Image.open(path)
        exif = img.getexif()
        if not exif:
            return {}
        # Convert to simple dict of numeric keys to values
        return {k: exif.get(k) for k in exif}
    except Exception:
        return {}


# Optional semantic image labeling (CLIP) — used when OCR returns nothing
try:
    from transformers import CLIPProcessor, CLIPModel
    import torch
    _CLIP_AVAILABLE = True
except Exception:
    CLIPProcessor = None  # type: ignore
    CLIPModel = None  # type: ignore
    torch = None  # type: ignore
    _CLIP_AVAILABLE = False


def label_image_semantic(path: str, top_k: int = 5) -> list[str]:
    """Return simple text labels for an image using CLIP if available.

    This is optional and only runs when CLIP is installed. It returns a list of
    short labels describing the image contents.
    """
    if not _CLIP_AVAILABLE:
        return []
    try:
        processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
        model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
        image = Image.open(path).convert('RGB')
        inputs = processor(images=image, return_tensors='pt')
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        # This is a placeholder: CLIP gives embeddings — to get labels we'd need
        # to compare to a candidate set. For now, return an empty list to keep
        # the function safe. Replace with a candidate-label approach as needed.
        return []
    except Exception:
        return []
