import click


class CLIBase(click.Context):
    test: str = "pass"
