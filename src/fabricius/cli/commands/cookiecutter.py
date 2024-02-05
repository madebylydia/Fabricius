# pylint: disable=R0913,R0914 # It's CookieCutter's stuff, what am I supposed to do?

import pathlib
from typing import Literal

import click
import rich
from rich.prompt import Confirm

from fabricius.exceptions.invalid_template.invalid_config import InvalidConfigException
from fabricius.exceptions.invalid_template.missing_config import MissingConfigException
from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.readers.cookiecutter.builder import CookieCutterBuilder
from fabricius.readers.cookiecutter.hooks import get_hooks


def validate_extra_context(_: click.Context, __: str, context_value: str):
    """Validate extra context."""
    values: dict[str, str] = {}
    for string in context_value:
        if "=" not in string:
            raise click.BadParameter('Syntax: "key=value".\n' f'"{string}" is invalid.')
        key, value = string.split("=")
        values[key] = value
    return values


# List of options here:
# https://github.com/cookiecutter/cookiecutter/blob/5d2b1e37b90ad11ac412c691f131689445840709/cookiecutter/cli.py#L70-L153
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
def cookiecutter(
    name_or_path: str,
    output_folder: str,
    extra_context: dict[str, str],
    *,
    no_input: bool,
    overwrite: bool,
    accept_hooks: Literal["yes", "ask", "no"],
    keep_on_failure: bool,
) -> None:
    """Run a CookieCutter template.

    Mimics the CookieCutter CLI options.

    [ ] config_file
    [ ] default_config
    [ ] skip_if_file_exists
    """
    console = rich.get_console()

    input_path = pathlib.Path(name_or_path).resolve()
    output_path = pathlib.Path(output_folder).resolve()

    try:
        builder = CookieCutterBuilder(input_path, output_path)
    except MissingConfigException:
        console.print(
            "[red]It appears that this path does not contain any [bold]cookiecutter.json[/] file."
        )
        console.print("Please make sure that you are in the right folder and try again.")
        return
    except InvalidConfigException:
        console.print(
            "[red]It appears that your [bold]cookiecutter.json[/] file is invalid. Check the and "
            "try again."
        )
        return

    console.print(f"[green]Generating {input_path.name}...")

    builder.extra_context = extra_context

    if not no_input:
        answers: dict[str, str | None] = {}
        questions = builder.get_questions()
        for question in questions:
            answers[question.id] = question.ask()
        builder.answers = answers

    if accept_hooks == "ask":
        hooks = get_hooks(input_path)
        if (hooks["post_gen_project"] or hooks["pre_gen_project"]) and Confirm.ask(
            "There are hooks that can be connected, would you like to use them?"
        ):
            pass

    builder.delete_on_failure = not keep_on_failure

    try:
        builder.execute(overwrite)
    except PreconditionException as exception:
        console.print()
        console.print(
            "[red]Uhm, it appears that something went wrong during the generation of your "
            "project."
        )
        console.print(
            "Please ensure that [blue]your output directory is empty[/], or that you have "
            "[blue]allowed overwriting[/]."
        )
        console.print(f"[red]Exception message:[/] {exception}")
        return

    console.print(f"[green]Successfully generated {input_path.name}! :thumbsup:")
