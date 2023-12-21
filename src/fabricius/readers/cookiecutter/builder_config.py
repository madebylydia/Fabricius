import json
import pathlib
import typing
from fnmatch import fnmatch

from fabricius.composers.jinja import JinjaComposer
from fabricius.configurator.reader.cookiecutter import (
    CookieCutterConfigReader,
    CookieCutterExtra,
)
from fabricius.configurator.universal import UniversalConfig
from fabricius.models.file import File
from fabricius.readers.cookiecutter.types import WrappedInCookiecutter


def require_render(text: str) -> bool:
    """
    Add a cookiecutter tag to a text.

    Parameters
    ----------
    text : str
        The text to wrap.
    """
    return "{{" in text and "}}" in text


class CookieCutterBuilderConfig:
    """
    Utility class to manage the context of a cookiecutter template.
    """

    raw_context: dict[str, typing.Any]

    config: UniversalConfig[CookieCutterExtra]

    def __init__(self, file: pathlib.Path) -> None:
        self.config = CookieCutterConfigReader(file).obtain()
        self.raw_context = json.loads(file.resolve().read_text())

    def wrapped_in_cookiecutter(self) -> WrappedInCookiecutter:
        """
        Return the context wrapped in a cookiecutter key.
        """
        return {"cookiecutter": self.raw_context}

    def get_prompts(self) -> dict[str, typing.Any]:
        questions: dict[str, typing.Any] = {
            key: value
            for key, value in self.raw_context.items()
            if not key.startswith("_") or not require_render(value)
        }
        return questions

    def get_extensions(self) -> list[str]:
        return self.config.extra.get("_extensions", [])
