import click
from rich import get_console
from rich.table import Table

from fabricius.app.config import Config


@click.command()
def list():
    """
    List repositories stored by Fabricius.
    """
    console = get_console()
    config = Config.get()

    if len(config.stored_repositories) == 0:
        return console.print("There is no repository stored.")

    table = Table(title="Stored Repositories")

    table.add_column("Alias")
    table.add_column("Path")

    for alias, path in config.stored_repositories.items():
        table.add_row(alias, str(path))

    get_console().print(table)
