import abc
import string
from collections import UserDict
from typing import Any

import chevron

from fabricius.const import Data


class DictAllowMiss(UserDict[str, Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str):
        return ""


class Renderer(abc.ABC):
    data: Data
    """
    A dictionary that contains data passed by the users to pass inside the template.
    """

    def __init__(self, data: Data) -> None:
        self.data = data

    @abc.abstractmethod
    def render(self, content: str) -> str:
        raise NotImplementedError()


class PythonFormatRenderer(Renderer):
    def render(self, content: str) -> str:
        return content.format_map(DictAllowMiss(self.data))


class ChevronRenderer(Renderer):
    def render(self, content: str) -> str:
        return chevron.render(content, self.data)


class StringTemplateRenderer(Renderer):
    def render(self, content: str) -> str:
        return string.Template(content).safe_substitute(DictAllowMiss(self.data))
