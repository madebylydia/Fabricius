import typing

from rich.console import Console
from rich.theme import Theme

from .const import TerminalTheme
from .interfaces import Singleton
from .utils import calculate_text_color

if typing.TYPE_CHECKING:
    from rich.prompt import PromptBase


_PT = typing.TypeVar("_PT")


class Terminal(Singleton):
    console: "Console"
    """
    The console used to interact.
    """

    def __init__(self, *, theme: typing.Optional[Theme] = None):
        self.console = Console(theme=TerminalTheme)
        if theme:
            self.console.use_theme(theme, inherit=True)

    def _get_box_colors(self, color: str) -> str:
        return f"{calculate_text_color(color)} on {color}"

    @typing.overload
    def input(self, prompt: str) -> str:
        ...

    @typing.overload
    def input(self, prompt: str, *, prompt_type: "typing.Type[PromptBase[_PT]]") -> _PT:
        ...

    def input(
        self, prompt: str, *, prompt_type: "typing.Optional[typing.Type[PromptBase[_PT]]]" = None
    ) -> str | _PT:
        """
        Request the input of the user.

        Parameters
        ----------
        prompt : :py:class:`str`
            The question to the user.
        prompt_type : Optional, type of :py:class:`rich.prompt.PromptBase`
            The type of prompt. Passing this parameter will make use of the ``.ask`` method.
        """
        if prompt_type:
            return prompt_type.ask(f"[fabricius.input]{prompt}[/]")
        return self.console.input(f"[fabricius.input]{prompt}[/]: ")

    def title(self, name: str) -> None:
        """
        Print a title.

        Parameters
        ----------
        name : :py:class:`str`
            The title.
        """
        self.console.print(f"{name}", justify="center", style="fabricius.title")

    def empty(self):
        """
        Draw an empty line.
        """
        self.console.print()

    def warning(self, title: str, description: str) -> None:
        """
        Print a warning.

        Parameters
        ----------
        title : :py:class:`str`
            The title of the warning
        description : :py:class:`str`
            Its description, explains what's wrong.
        """
        self.console.print(f"[fabricius.warning.box] {title} [/] [fabricius.warning]{description}")

    def success(self, title: str, description: str) -> None:
        """
        Print a successful action.

        Parameters
        ----------
        title : :py:class:`str`
            A simple title
        description : :py:class:`str`
            Its description, explain what was successful.
        """
        self.console.print(f"[fabricius.success.box] {title} [/] [fabricius.success]{description}")

    def skip(self, title: str, description: str) -> None:
        """
        Print a skipped action.

        Parameters
        ----------
        title : :py:class:`str`
            The title of the skip
        description : :py:class:`str`
            Its description, explains what was skipped.
        """
        self.console.print(f"[fabricius.skip.box] {title} [/] [fabricius.skip]{description}")

    def overwrite(self, title: str, description: str) -> None:
        """
        Print an overwrite action.

        Parameters
        ----------
        title : :py:class:`str`
            The title of the overwrite
        description : :py:class:`str`
            Its description, explains what was overwritten.
        """
        self.console.print(
            f"[fabricius.overwrite.box] {title} [/] [fabricius.overwrite]{description}"
        )

    def exception(self, title: str, *, title_after: bool = False) -> None:
        """
        Print a title for an exception and the exception itself using Rich.

        Parameters
        ----------
        title : :py:class:`str`
            The title of the exception, giving more explanation on the error.
        title_after : :py:class:`bool`
            Indicates if the title should be printed before or after the exception has been printed
        """
        if not title_after:
            self.console.print(f" {title} ", style="fabricius.error")
        try:
            self.console.print_exception()
        except ValueError:
            self.warning("Cannot render exception", "No exception were raised.")
        if title_after:
            self.console.print(f" {title} ", style="fabricius.error")
