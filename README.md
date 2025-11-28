# HelpHive — AI-assisted folder/file renamer for macOS

Overview
 - This small Python CLI helps you organize folders by suggesting concise folder names derived from the files inside each folder. It extracts samples from text and PDF files and sends them to an AI model (OpenAI) to propose filesystem-friendly names.

Getting started

Prerequisites
 - Python 3.10+
 - An OpenAI API key set in the environment as `OPENAI_API_KEY` (or load via `.env` using `python-dotenv`).

Install dependencies
```bash
python -m pip install -r requirements.txt
```

Usage
 - Dry-run (safe):
```bash
python -m src.main /path/to/target/folder
```

 - Apply renames:
```bash
python -m src.main /path/to/target/folder --apply
```

Options
 - `--include-root-files` — also generate a name for files directly in the target folder (treats root files like a virtual folder)
 - `--model` — specify model name to use (defaults to `gpt-4`)

Notes & safety
 - The tool shows suggestions before renaming (dry-run by default). Review suggestions carefully before applying.
 - The AI may propose names you want to tweak; when using `--apply` the tool will still ask for confirmation per-folder.
 - Only simple text/PDF extraction is included. For other file types add custom extractors in `src/scanner.py`.

Next steps I can do
 - Add an option to rename individual files using per-file summarization.
 - Add a macOS GUI (Swift) wrapper that calls this CLI under the hood.
 - Add unit tests and more file-type extractors (images, Office formats).
