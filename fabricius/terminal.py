from .const import Colors
from .interfaces import Singleton
from .utils import calculate_text_color

import typing
import rich


if typing.TYPE_CHECKING:
    from rich.prompt import PromptBase
    from rich.console import Console


_PT = typing.TypeVar("_PT")


class Terminal(Singleton):
    _console: "Console"
    """
    The console used to interact.
    """

    _colors: typing.Type[Colors]
    """
    The colors to use with renderer text
    """

    def __init__(self, *, colors: typing.Type[Colors] = Colors):
        self._console = rich.get_console()
        self._colors = colors

    @typing.overload
    def input(self, prompt: str) -> str:
        ...

    @typing.overload
    def input(self, prompt: str, *, prompt_type: "typing.Type[PromptBase[_PT]]") -> _PT:
        ...

    def input(self, prompt: str, *, prompt_type: "typing.Optional[typing.Type[PromptBase[_PT]]]" = None) -> str | _PT:
        """
        Request the input of the user.

        Parameters
        ----------
        prompt : str
            The question to the user.

        Returns
        -------
        str :
            The user's input/answer.
        """
        if prompt_type:
            return prompt_type.ask(f"[{self._colors.INPUT}]{prompt}[/]")
        return self._console.input(f"[{self._colors.INPUT}]{prompt}[/]: ")

    def title(self, name: str):
        """
        Print a title.

        Parameters
        ----------
        name : str
            The title.
        """
        self._console.print(f"{name}", justify="center", style=f"white on {self._colors.TITLE}")

    def empty(self):
        """
        Draw an empty line.
        """
        self._console.print()

    def warning(self, title: str, description: str):
        """
        Print a warning.

        Parameters
        ----------
        title : str
            The title of the warning
        description : str
            Its description, explains what's wrong.
        """
        self._console.print(f"[{calculate_text_color(self._colors.WARNING)} on {self._colors.WARNING}] {title} [/] [{self._colors.WARNING}]{description}")

    def success(self, title: str, description: str):
        """
        Print a successful action.

        Parameters
        ----------
        title : str
            A simple title
        description : str
            Its description, explain what was successful.
        """
        self._console.print(f"[{calculate_text_color(self._colors.SUCCESS)} on {self._colors.SUCCESS}] {title} [/] [{self._colors.SUCCESS}]{description}")

    def skip(self, title: str, description: str):
        """
        Print a skipped action.

        Parameters
        ----------
        title : str
            The title of the skip
        description : str
            Its description, explains what was skipped.
        """
        self._console.print(f"[{calculate_text_color(self._colors.SKIP)} on {self._colors.SKIP}] {title} [/] [{self._colors.SKIP}]{description}")

    def overwrite(self, title: str, description: str):
        """
        Print an overwrite action.

        Parameters
        ----------
        title : str
            The title of the overwrite
        description : str
            Its description, explains what was overwrote.
        """
        self._console.print(f"[{calculate_text_color(self._colors.OVERWRITE)} on {self._colors.OVERWRITE}] {title} [/] [{self._colors.OVERWRITE}]{description}")


    def exception(self, title: str, *, title_after: bool = False):
        """
        Print a title for an exception and the exception itself using Rich.

        Parameters
        ----------
        title : str
            The title of the exception, giving more explanation on the error.
        title_after : bool
            Indicates if the title should be printed before or after the exception has been printed
        """
        if not title_after:
            self._console.print(f" {title} ", style=f"{calculate_text_color(self._colors.ERROR)} on {self._colors.ERROR}")
        try:
            self._console.print_exception()
        except ValueError:
            self.warning("Cannot render exception", "No exception were raised.")
        if title_after:
            self._console.print(f" {title} ", style=f"{calculate_text_color(self._colors.ERROR)} on {self._colors.ERROR}")
