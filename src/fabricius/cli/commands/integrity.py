import pathlib
import shutil

import click
from rich import get_console
from rich.prompt import Confirm

from fabricius.app.config import Config


@click.command()
def integrity():
    """
    Check Fabricius's Config integrity.
    """
    found_integrity_issues = 0
    resolved_integrity_issues = 0
    console = get_console()
    config = Config.get()

    # Ensure all folders are present from config

    folders_lost: dict[str, pathlib.Path] = {}

    for alias, path in config.stored_repositories.items():
        if not path.exists():
            found_integrity_issues += 1
            folders_lost[alias] = path

    for alias, path in folders_lost.items():
        get_console().print(f"Folder {path} was lost for alias {alias}")

        if Confirm.ask(f"Delete {alias} from config?"):
            config.stored_repositories.pop(alias)
            resolved_integrity_issues += 1

    # Ensure no new folders have been added without getting stored.

    unknown_folders: list[pathlib.Path] = []

    for path in config.download_path.iterdir():
        if path.is_dir() and path not in config.stored_repositories.values():
            unknown_folders.append(path)
            found_integrity_issues += 1

    if unknown_folders:
        console.print(f"{len(unknown_folders)} folders are unknown to Fabricius.")
        console.print("\n".join(f"-> {path.resolve()}" for path in unknown_folders))

        if Confirm.ask("Delete these folders?"):
            for path in unknown_folders:
                shutil.rmtree(path)
                resolved_integrity_issues += 1

    if not found_integrity_issues:
        console.print("No integrity issues found. Great!")
    else:
        config.persist()
        console.print(
            f"Found {found_integrity_issues} integrity issues in Config."
            f" {resolved_integrity_issues} of them were resolved automatically."
        )
