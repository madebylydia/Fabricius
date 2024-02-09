from fabricius.models.composer import Composer


class CopyComposer(Composer):
    """A simple composer that copies the content with no special rendering.
    Can be useful to use with files that are specified to not be rendered.
    """

    name = "Copy"

    def render(self, content: str) -> str:
        return content
