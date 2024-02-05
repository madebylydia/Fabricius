import logging
import pathlib
import typing

import ccl
import click
import rich
from rich.logging import RichHandler
from rich.prompt import Confirm

import fabricius
from fabricius.app.config import Config, get_or_create_default_config
from fabricius.app.error_reporter import can_report, report_exception

_log = logging.getLogger("fabricius")

SUPPRESSED_MODULES = [click]


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="WARNING",
)
@click.version_option(fabricius.__version__)
@click.pass_context
def cli(
    ctx: click.Context, log_level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
):
    logging.basicConfig(
        level=log_level,
        format="%(name)s (%(funcName)s) : %(message)s",
        handlers=[
            RichHandler(markup=True, rich_tracebacks=True, tracebacks_suppress=SUPPRESSED_MODULES)
        ],
        datefmt="%H:%M:%S",
    )
    _log.root.setLevel(log_level)
    _log.info("Log have been set to %s.", log_level)

    ctx.ensure_object(dict)
    ctx.obj["config"] = Config.load(get_or_create_default_config())

    rich.get_console().clear()


def main():
    # aspreno.register_global_handler(aspreno.ExceptionHandler())
    ccl.register_commands(cli, pathlib.Path(__file__, "..", "commands").resolve(), "file")

    try:
        cli()  # pylint: disable=E1120
    except Exception as exception:  # pylint: disable=W0718
        console = rich.get_console()
        console.print_exception(suppress=SUPPRESSED_MODULES)
        console.print("\n[bold]❌ Sorry! Fabricius has crashed *really* hard.")
        console.print("[bold red]This error was not handled.[/]")
        console.print(
            "You should report this issue to the developers at "
            "[blue underline]https://github.com/madebylydia/Fabricius[/]"
        )

        if can_report():
            console.print(
                "\n\nAs you have installed the Sentry SDK, you have the ability to automatically "
                "report this issue to the developers."
            )
            console.print(
                "For more information about your privacy, please visit "
                "[blue underline]https://sentry.io/security/[/]"
            )
            console.print("No personnal information will be collected.")

            if Confirm.ask("Would you like to send this exception to the developers?"):
                report_exception(exception)
                console.print("The exception has been sent to the developers. Thank you!")
