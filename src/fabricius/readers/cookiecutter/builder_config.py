import typing
from fnmatch import fnmatch

from fabricius.composers.jinja import JinjaComposer
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
    """
    The context containing data.
    """

    def __init__(self, context: dict[str, typing.Any]) -> None:
        self.raw_context = context

    def should_copy(self, file: File):
        """
        Determine if a file should be copied or rendered.

        Parameters
        ----------
        file : :py:class:`File <fabricius.models.file.File>`
            The file we're checking.
        """
        # TODO: To rewrite, so it use a rendered context.
        if not self.raw_context["cookiecutter"].get("_copy_without_render"):
            return False
        to_ignore: list[str] = self.raw_context["_copy_without_render"]
        for index, value in enumerate(to_ignore):
            to_ignore[index] = (
                JinjaComposer().push_data(self.wrapped_in_cookiecutter()).render(value)
            )
        return any(fnmatch(str(file.compute_destination()), value) for value in to_ignore)

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

    def get_default_context(self) -> dict[str, typing.Any]:
        """
        Return the default context provided in the context.
        Used to fill up the defaults.
        """
        return self.raw_context.get("default_context", {})

    def get_extensions(self) -> list[str]:
        return self.raw_context.get("_extensions", [])
