from fabricius.models.composer import Composer
from fabricius.utils import DictAllowMiss


class PythonFormatComposer(Composer):
    """Composer using :py:meth:`str.format` to render the content."""

    name = "Python str.format"

    def render(self, content: str) -> str:
        return content.format_map(DictAllowMiss(self.data))
