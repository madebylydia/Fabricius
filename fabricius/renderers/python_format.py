from fabricius.models.renderer import Renderer

from .utils import DictAllowMiss


class PythonFormatRenderer(Renderer):
    name = "Python str.format"

    def render(self, content: str) -> str:
        return content.format_map(DictAllowMiss(self.data))
