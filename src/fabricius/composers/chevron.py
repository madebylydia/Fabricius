import chevron

from fabricius.models.composer import Composer


class ChevronComposer(Composer):
    name = "Chevron (Moustache)"

    def render(self, content: str) -> str:
        return chevron.render(content, dict(self.data))
