import pathlib

import click
import rich

from fabricius.exceptions import TemplateError
from fabricius.readers.cookiecutter.setup import run as cookiecutter_run
from fabricius.readers.cookiecutter.setup import setup


@click.command()
@click.argument("name_or_path")
@click.argument("output_folder")
@click.option("--overwrite", is_flag=True)
def run(name_or_path: str, output_folder: str):
    """
    Run a CookieCutter template.

    Mimics the CookieCutter CLI.
    """
    console = rich.get_console()

    try:
        input_path = pathlib.Path(name_or_path).resolve()
        output_path = pathlib.Path(output_folder).resolve()
    except Exception as e:
        return print(e)
    try:
        template = setup(input_path, output_path)
    except TemplateError as error:
        click.echo(f"Error while setting up template: {error}")
        return
    cookiecutter_run(template)

    console.print(f"[green]Successfully generated {input_path.name}! :thumbsup:")
