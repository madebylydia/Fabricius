import dataclasses
import pathlib
import typing

from rich import get_console
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt, PromptBase


@dataclasses.dataclass(kw_only=True)
class QuestionConfig:
    id: str
    """
    The "ID" of the question.

    This is what is used to fill the data's keys, and what should be used to refer to the
    question's value inside a template.
    """

    help: str | None
    """
    An optional help string to show to the user.
    Supports `Rich's console markup <https://rich.readthedocs.io/en/stable/markup.html>`.

    This string will be shown just once and before the prompt.
    To edit the prompt, use the "prompt" attribute.
    """

    prompt: str | None
    """
    The question to ask when prompting to the user.
    Supports `Rich's console markup <https://rich.readthedocs.io/en/stable/markup.html>`.

    If None, the question's ID will be used.
    """

    type: typing.Any | None
    """
    The type the question must be.

    Supported types:
    - str
    - bool
    - int
    - float
    """

    default: typing.Any | None
    """
    The default value of the question.

    If None, the user will be prompted to answer the question.
    """

    hidden: bool
    """
    If the question should be shown to the user.
    """

    factory: typing.Callable[[str], typing.Any] | None
    """
    An optional function that is ran after the user's answer is received.
    Used to transform the answer into something else.
    """

    choices: list[str] | None
    """
    A list of choices for the user to pick from.

    If None, the user is free to pass anything.
    """

    def _get_prompt(self) -> PromptBase[typing.Any]:
        """
        Obtain the right prompt correspoding to the given type.

        Returns
        -------
        PromptBase
            The prompt to use.
        """
        if self.type == bool:
            return Confirm(self.prompt or self.id)
        elif self.type == int:
            return IntPrompt(self.prompt or self.id)
        elif self.type == float:
            return FloatPrompt(self.prompt or self.id)
        else:
            return Prompt(self.prompt or self.id)

    def ask(self) -> str | None:
        """
        Ask the question to the user.

        Returns
        -------
        str
            The user's answer.
        """
        if self.hidden:
            return None

        console = get_console()
        if self.help:
            console.print(self.help)
        prompt = self._get_prompt()
        if self.default:
            answer = prompt.ask(self.prompt or self.id, choices=self.choices, default=self.default)
        else:
            answer = prompt.ask(self.prompt or self.id, choices=self.choices)

        return self.factory(str(answer)) if self.factory else str(answer)


@dataclasses.dataclass(kw_only=True)
class UniversalConfig[Extra: typing.Mapping[str, typing.Any]]:
    root: pathlib.Path
    """
    The source of the template.
    """

    destination: pathlib.Path
    """
    The given destination of the template.

    No extra sub-folders will be created.
    """

    questions: "list[QuestionConfig]"
    """
    A list of questions to ask to the users.
    """

    extra: "Extra"
    """
    An attribute that comes unused to the user, but that can be used to store extra metadata.
    (Eg. CookieCutter's extensions, Jinja's environment settings, etc.)
    """
