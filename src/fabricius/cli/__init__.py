import logging
import pathlib
import typing

import aspreno
import ccl
import click
from rich.logging import RichHandler

from fabricius.app.config import Config, get_or_create_default_config

_log = logging.getLogger("fabricius")


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="WARNING",
)
@click.pass_context
def cli(
    ctx: click.Context, log_level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
):
    logging.basicConfig(
        level=log_level,
        format="%(name)s (%(funcName)s) : %(message)s",
        handlers=[RichHandler()],
        datefmt="%H:%M:%S",
    )
    _log.root.setLevel(log_level)
    _log.info(f"Log have been set to {log_level}.")

    ctx.ensure_object(dict)
    ctx.find_object(Config)
    ctx.obj["config"] = Config.load(get_or_create_default_config())


def main():
    aspreno.register_global_handler(aspreno.ExceptionHandler())
    ccl.register_commands(cli, pathlib.Path(__file__, "..", "commands").resolve(), "file")

    cli()
