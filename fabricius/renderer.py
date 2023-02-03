import abc
import string
import typing
from collections import UserDict

import chevron

from fabricius.const import Data


class DictAllowMiss(UserDict[str, typing.Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str) -> typing.Literal[""]:
        return ""


class Renderer(abc.ABC):
    name: typing.Optional[str]
    """
    The name of the renderer, not necessary, but suggested to add.
    """

    data: Data
    """
    A dictionary that contains data passed by the users to pass inside the template.
    """

    def __init__(self, data: Data) -> None:
        """

        Parameters
        ----------
        data : Data
            The data to pass to the renderer.
        """
        self.data = data

    @abc.abstractmethod
    def render(self, content: str) -> str:
        """
        This method will process a given string, the template input and return the processed
        template as a string too.

        Parameters
        ----------
        content : str
            The template

        Returns
        -------
        str :
            The result of the processed template.
        """
        raise NotImplementedError()


class PythonFormatRenderer(Renderer):
    name = "Python str.format"

    def render(self, content: str) -> str:
        return content.format_map(DictAllowMiss(self.data))


class ChevronRenderer(Renderer):
    name = "Chevron (Moustache)"

    def render(self, content: str) -> str:
        return chevron.render(content, self.data)


class StringTemplateRenderer(Renderer):
    name = "Python string.Template"

    safe: bool
    """
    Indicate if the renderer should use
    :py:meth:`string.Template.safe_substitute` or
    :py:meth:`string.Template.substitute`
    """

    def __init__(self, data: Data, *, safe: bool = True) -> None:
        self.safe = safe
        super().__init__(data)

    def render(self, content: str) -> str:
        if self.safe:
            return string.Template(content).safe_substitute(DictAllowMiss(self.data))
        else:
            return string.Template(content).substitute(self.data)
