import os
from typing import Optional
from PyPDF2 import PdfReader


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
