import os
import pathlib

import click
from rich import get_console
from rich.table import Table
from rich.text import Text

from fabricius.config import Config

from .utils import available_internal_templates


@click.command("templates")
@click.option(
    "--working-directory",
    required=False,
    type=pathlib.Path,
    default=lambda: os.getcwd(),
    show_default="Where the command is ran",
    help="Where to look for internal templates",
)
def cmd_templates(*, working_directory: pathlib.Path):
    """
    List available templates.
    """
    console = get_console()
    # config = Config.get_config()

    templates = available_internal_templates(at=working_directory)
    # Todo: Add external templates

    if not templates:
        console.print("[red]Oh no! :( No templates were found.")
        return

    table = Table(title="Available templates", show_lines=True)
    table.add_column("Template Name", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Type", justify="center")

    for template in templates:
        # Get the right color for template's type
        template_type = Text(
            template.type.title(),
            "red" if template.type == "internal" else "yellow",
        )
        # Add the template to the table
        table.add_row(template.name, str(template.path.resolve()), template_type)

    # Don't think that's relevant for now...
    # console.print("[blue]Note:[/blue] [red]Internal[/red] templates are in your folder, [yellow]External[/yellow] templates are stored by Fabricius.", end="\n\n")
    console.print(table)
