import os
import shutil
from typing import Optional
from .scanner import sample_texts_in_folder
from .ai_client import suggest_folder_name


def _slugify(name: str) -> str:
    keep = []
    for ch in name:
        if ch.isalnum() or ch in (' ', '-', '_'):
            keep.append(ch)
    s = ''.join(keep).strip()
    s = s.replace(' ', '_')
    # collapse multiple underscores
    while '__' in s:
        s = s.replace('__', '_')
    return s or 'renamed'


def safe_rename(src: str, dst: str) -> bool:
    try:
        shutil.move(src, dst)
        return True
    except Exception:
        return False


def propose_rename_folder(folder_path: str, dry_run: bool = True, model: str = 'gpt-4') -> Optional[str]:
    samples = sample_texts_in_folder(folder_path)
    suggestion = suggest_folder_name(samples, model=model)
    if not suggestion:
        return None

    new_name = _slugify(suggestion)

    parent = os.path.dirname(folder_path)
    target = os.path.join(parent, new_name)

    # If target exists, append a numeric suffix
    if os.path.exists(target):
        base = new_name
        i = 1
        while os.path.exists(os.path.join(parent, f"{base}_{i}")):
            i += 1
        target = os.path.join(parent, f"{base}_{i}")

    if dry_run:
        return target

    ok = safe_rename(folder_path, target)
    return target if ok else None
