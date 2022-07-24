import string
from collections import UserDict
from typing import Any

import chevron

from fabricius.contracts import RendererContract


class DictAllowMiss(UserDict[str, Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str):
        return ""


class PythonFormatRenderer(RendererContract):
    def render(self, content: str) -> str:
        return content.format_map(DictAllowMiss(self.data))


class ChevronRenderer(RendererContract):
    def render(self, content: str) -> str:
        return chevron.render(content, self.data)


class StringTemplateRenderer(RendererContract):
    def render(self, content: str) -> str:
        return string.Template(content).safe_substitute(DictAllowMiss(self.data))
