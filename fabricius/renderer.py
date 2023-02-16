import abc
import string
import typing
from collections import UserDict

import chevron

from .const import Data


class DictAllowMiss(UserDict[str, typing.Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str) -> typing.Literal[""]:
        return ""


class Renderer(abc.ABC):
    """
    The Renderer is what translate and generates the output of templates. Core of the work.

    You must subclass this class and override the :py:meth:`render` method, if possible, also add
    a name.
    """

    name: typing.Optional[str]
    """
    The name of the renderer, not necessary, but suggested to add.
    """

    data: Data
    """
    A dictionary that contains data passed by the users to pass inside the template.
    """

    def __init__(self, data: Data) -> None:
        self.data = data

    @abc.abstractmethod
    def render(self, content: str) -> str:
        """
        This method will process a given string, the template input and return the processed
        template as a string too.

        Parameters
        ----------
        content : :py:class:`str`
            The template

        Returns
        -------
        :py:class:`str` :
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
