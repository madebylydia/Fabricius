from .interfaces import Singleton

import typing
import rich
from rich.console import Console


class Terminal(Singleton):
    _console: Console
    """
    The console used to interact.
    """

    def __init__(self):
        self._console = rich.get_console()

    def input(self, prompt: str, color: typing.Optional[str]):
        self._console.input(f"{'[' + color + ']' if color else ''}{prompt}")

    def title(self, name: str, color: str):
        """
        Print a title.
        """
        self._console.print(f"{name}", justify="center", style=f"white on {color}")

    def empty(self):
        """
        Draw an empty line.
        """
        self._console.print()

    def action(self, name: str, color: str, description: typing.Optional[str] = None):
        """
        Print an action.
        """
        self._console.print(f"[on {color}] {name} [/] [{color}]{description}")
