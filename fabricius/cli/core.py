from typing import List

import click

from .make import cmd_make
from .templates import cmd_templates


@click.group("fabricius")
def run():
    """
    Fabricius - Python Templating Engine
    """


SUB_COMMANDS: List[click.Command] = [cmd_make, cmd_templates]

for command in SUB_COMMANDS:
    run.add_command(command, command.name)
