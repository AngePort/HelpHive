import os
from typing import Optional
import openai


def get_api_key():
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY not set in environment')
    return key


def suggest_folder_name(samples: list[str], model: str = 'gpt-4', max_tokens: int = 64) -> Optional[str]:
    """Send the collected samples to the AI and request a concise folder name suggestion.

    Returns a short suggested name or None on failure.
    """
    if not samples:
        return None

    openai.api_key = get_api_key()

    # Build a short prompt giving the model context and asking for a short name
    prompt = (
        "You are given several representative snippets of files contained in a folder.\n"
        "Suggest a concise, filesystem-friendly folder name (3 words max) that best describes the folder's contents.\n"
        "Return only the suggested name, no punctuation, no explanation.\n\n"
    )

    # include up to a few samples
    body = prompt + '\n\nSamples:\n' + ('\n\n'.join(samples[:6]))

    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": body}],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        text = resp.choices[0].message.content.strip()
        # sanitize common noise
        return text.splitlines()[0].strip(' "')
    except Exception:
        return None
