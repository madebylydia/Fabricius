import os
import pathlib

import click


@click.command("make")
@click.argument("template")
@click.option(
    "--working-directory",
    required=False,
    type=pathlib.Path,
    default=lambda: os.getcwd(),
    show_default="Where the command is ran",
    help="Where to look for internal templates",
)
def cmd_make(template: str, *, working_directory: pathlib.Path):
    """
    Run a template. (make it!)
    """
    print(f"Welcome to make! You have selected {template}")
    print(f"Working directory: {working_directory.absolute()}")
