import logging
import pathlib
import typing

import aspreno
import ccl
import click

_log = logging.getLogger("fabricius")


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="WARNING",
)
def cli(log_level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]):
    logging.basicConfig()
    _log.setLevel(log_level)
    _log.root.setLevel(log_level)
    _log.info(f"Log have been set to {log_level}.")


def main():
    aspreno.register_global_handler(aspreno.ExceptionHandler())
    ccl.register_commands(cli, pathlib.Path(__file__, "..", "commands").resolve())

    cli()
