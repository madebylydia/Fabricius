import string

from fabricius.models.composer import Composer
from fabricius.utils import DictAllowMiss


class StringTemplateComposer(Composer):
    """Composer using ``string.Template`` to render the content."""

    name = "Python string.Template"

    safe: bool
    """
    Indicate if the composer should use
    :py:meth:`string.Template.safe_substitute` or
    :py:meth:`string.Template.substitute`.
    """

    def __init__(self, *, safe: bool = True) -> None:
        self.safe = safe
        super().__init__()

    def render(self, content: str) -> str:
        if self.safe:
            return string.Template(content).safe_substitute(DictAllowMiss(self.data))
        return string.Template(content).substitute(self.data)
