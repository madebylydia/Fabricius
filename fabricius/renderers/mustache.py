import chevron

from fabricius.models.renderer import Renderer


class ChevronRenderer(Renderer):
    name = "Chevron (Moustache)"

    def render(self, content: str) -> str:
        return chevron.render(content, self.data)
