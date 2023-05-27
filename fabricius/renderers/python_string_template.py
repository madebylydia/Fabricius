import string

from fabricius.models.renderer import Renderer
from fabricius.types import Data

from .utils import DictAllowMiss


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
