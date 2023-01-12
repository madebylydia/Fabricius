import abc
import string
from collections import UserDict
from typing import Any, Literal, Optional

import chevron

from fabricius.const import Data


class DictAllowMiss(UserDict[str, Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str) -> Literal[""]:
        return ""


class Renderer(abc.ABC):
    name: Optional[str]
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
        The method that will process a given template input and return a
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
    :py:obj:`python:string.Template.safe_substitute` or
    :py:obj:`python:string.Template.substitute`
    """

    def __init__(self, data: Data, *, safe: bool = True) -> None:
        self.safe = safe
        super().__init__(data)

    def render(self, content: str) -> str:
        if self.safe:
            return string.Template(content).safe_substitute(DictAllowMiss(self.data))
        else:
            return string.Template(content).substitute(self.data)
