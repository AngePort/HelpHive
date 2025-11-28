import argparse
import os
import sys
from rich.console import Console
from rich.prompt import Confirm, Prompt

from .renamer import propose_rename_folder


console = Console()


def find_folders(target: str, include_root_files: bool = False):
    # list immediate subfolders
    entries = os.listdir(target)
    folders = []
    for e in entries:
        p = os.path.join(target, e)
        if os.path.isdir(p):
            folders.append(p)

    if include_root_files:
        # treat root as a virtual folder for files directly inside target
        folders.insert(0, target)

    return folders


def main():
    parser = argparse.ArgumentParser(description='AI-assisted folder renamer')
    parser.add_argument('path', help='Target folder to analyze')
    parser.add_argument('--apply', action='store_true', help='Actually perform renames (default is dry-run)')
    parser.add_argument('--model', default='gpt-4', help='Model name to use for suggestions')
    parser.add_argument('--include-root-files', action='store_true', help='Also generate a name for files in the target root')

    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if not os.path.isdir(target):
        console.print(f'[red]Path not found or not a directory:[/] {target}')
        sys.exit(1)

    folders = find_folders(target, include_root_files=args.include_root_files)
    console.print(f'Found {len(folders)} folders to inspect.')

    for f in folders:
        console.print(f'\n[bold]Inspecting:[/] {f}')
        suggestion_path = propose_rename_folder(f, dry_run=not args.apply, model=args.model)
        if not suggestion_path:
            console.print('[yellow]No suggestion generated.[/] Skipping.')
            continue

        suggested_name = os.path.basename(suggestion_path)
        console.print(f'[cyan]Suggested name:[/] {suggested_name}')

        if not args.apply:
            do = Confirm.ask('Apply this rename? (this is a dry-run unless --apply passed)', default=False)
            if not do:
                console.print('Skipped.')
                continue

        # If we reach here and apply==True, perform the rename
        if args.apply:
            result = propose_rename_folder(f, dry_run=False, model=args.model)
            if result:
                console.print(f'[green]Renamed to:[/] {os.path.basename(result)}')
            else:
                console.print('[red]Rename failed.[/]')


if __name__ == '__main__':
    main()
