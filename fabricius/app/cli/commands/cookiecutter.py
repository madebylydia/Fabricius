import pathlib
from typing import Literal

import click
import rich
from rich.prompt import Confirm

from fabricius.exceptions import TemplateError
from fabricius.readers.cookiecutter.hooks import get_hooks
from fabricius.readers.cookiecutter.setup import connect_hooks
from fabricius.readers.cookiecutter.setup import run as cookiecutter_run
from fabricius.readers.cookiecutter.setup import setup


def validate_extra_context(ctx: click.Context, param: str, context_value: str):
    """Validate extra context."""
    values: dict[str, str] = {}
    for string in context_value:
        if "=" not in string:
            raise click.BadParameter('Syntax: "key=value".\n' f'"{string}" is invalid.')
        key, value = string.split("=")
        values[key] = value
    return values


@click.command()
@click.argument("name_or_path")
@click.argument("extra_context", nargs=-1, callback=validate_extra_context)
@click.option("--output-folder", default=".")
@click.option("--overwrite", is_flag=True)
@click.option("--no-input", is_flag=True)
@click.option(
    "--accept-hooks", type=click.Choice(["yes", "ask", "no"], False), multiple=False, default="ask"
)
@click.option("--keep-on-failure", is_flag=True)
def run(
    name_or_path: str,
    output_folder: str,
    extra_context: dict[str, str],
    *,
    no_input: bool,
    overwrite: bool,
    accept_hooks: Literal["yes", "ask", "no"],
    keep_on_failure: bool,
) -> None:
    """
    Run a CookieCutter template.

    Mimics the CookieCutter CLI options.

    [ ] verbose,
    [ ] config_file,
    [ ] default_config,
    [ ] skip_if_file_exists,
    """
    console = rich.get_console()

    input_path = pathlib.Path(name_or_path).resolve()
    output_path = pathlib.Path(output_folder).resolve()

    try:
        template = setup(
            input_path,
            output_path,
            allow_hooks=accept_hooks == "yes",
            extra_context=extra_context,
            no_prompt=no_input,
        )
    except TemplateError as error:
        click.echo(f"Error while setting up template: {error}")
        return

    if accept_hooks == "ask":
        hooks = get_hooks(input_path)
        if (hooks["post_gen_project"] or hooks["pre_gen_project"]) and Confirm.ask(
            "There are hooks that can be connected, would you like to use them?"
        ):
            connect_hooks(hooks)

    cookiecutter_run(template, overwrite=overwrite, keep_on_failure=keep_on_failure)

    console.print(f"[green]Successfully generated {input_path.name}! :thumbsup:")
