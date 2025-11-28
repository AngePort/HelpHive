import os
import tempfile

from src import renamer


def test_propose_rename_dryrun(monkeypatch):
    # Create a temporary folder with a sample text file
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "ProjectA")
        os.makedirs(folder)
        sample_path = os.path.join(folder, "notes.txt")
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write("Invoices and billing details for Acme Corp")

        # Monkeypatch the suggestion function to avoid network calls
        monkeypatch.setattr(renamer, "suggest_folder_name", lambda samples, model='gpt-4': "Invoices")

        # Dry-run should return a proposed target path but not perform the rename
        proposed = renamer.propose_rename_folder(folder, dry_run=True)
        assert proposed is not None
        assert os.path.basename(proposed).startswith("Invoices")
