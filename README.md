# HelpHive — AI-assisted folder renamer for macOS

Overview
 - HelpHive is a small Python CLI that scans folders and suggests concise, filesystem-friendly folder names using AI. It analyzes the contents of each folder (text, PDFs, and images via OCR when available) and proposes a better name when appropriate.

Current behavior
 - The tool scans only subfolders of the target directory (folder-level renaming). It does not rename individual files yet — file-level renaming is planned for a future update.
 - If the current folder name already matches the detected contents, the tool skips that folder and does not produce a suggestion.

Prerequisites (what you need installed / prepared)
 - `Python 3.10+` and `pip`.
 - A virtual environment is recommended (`python3 -m venv .venv`).
 - An OpenAI API key available in your environment as `OPENAI_API_KEY` (or load it from a local `.env` using `python-dotenv`).
 - Optional (for image OCR): the Tesseract binary on macOS:
	 - Install via Homebrew: `brew install tesseract`.
 - Recommended: keep `.env` in `.gitignore` if you store the key locally.

Install dependencies
```bash
# from project root
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Usage (examples)
 - Dry-run (safe; shows suggestions and prompts but does not rename unless you confirm and use `--apply`):
```bash
. .venv/bin/activate
python -m src.main /path/to/target/folder
```

 - Apply renames (will still ask per-folder confirmation):
```bash
python -m src.main /path/to/target/folder --apply
```

 - Include files directly under the target folder as a single virtual folder:
```bash
python -m src.main /path/to/target/folder --include-root-files
```

What the tool does
 - Walks each immediate subfolder of the provided target folder.
 - Extracts readable content (text files, PDFs, OCR from images if Tesseract is available).
 - Sends representative samples to the AI and asks for a short, filesystem-safe folder name.
 - Proposes a filesystem-safe name; if a name already exists, it will suggest a suffixed name to avoid collisions.

Safety & notes
 - Default is dry-run: nothing will be renamed unless you pass `--apply` and confirm the prompts.
 - The AI may return suggestions that need human review — always verify before applying broadly.
 - The scanner currently prioritizes folder-level summaries; improving per-file renaming and richer image semantics is planned.

Further improvements planned
 - Per-file renaming mode (rename files individually based on content).
 - Better image semantic labeling (CLIP or vision APIs) for photo-only folders.
 - A lightweight macOS GUI wrapper to run the CLI with point-and-click controls.

