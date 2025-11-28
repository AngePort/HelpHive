import os
import tempfile

from src import renamer


def test_propose_rename_dryrun(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        folder = os.path.join(tmp, "ProjectA")
        os.makedirs(folder)
        with open(os.path.join(folder, "notes.txt"), "w", encoding="utf-8") as f:
            f.write("Invoices and billing details for Acme Corp")

        monkeypatch.setattr(renamer, "suggest_folder_name", lambda samples, model='gpt-4': "Invoices")

        proposed = renamer.propose_rename_folder(folder, dry_run=True)
        assert proposed is not None
        assert os.path.basename(proposed).startswith("Invoices")
