import chevron

from fabricius.models.composer import Composer


class ChevronComposer(Composer):
    """Composer using ``chevron`` to render the content."""

    name = "Chevron (Moustache)"

    def render(self, content: str) -> str:
        return chevron.render(content, dict(self.data))
