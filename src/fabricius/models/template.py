import pathlib
import typing

if typing.TYPE_CHECKING:
    from fabricius.models.file import File

TemplateState = typing.Literal["pending", "failed", "persisted", "deleted"]


class Template:
    """The template class represent the base of an application.
    This is what Fabricius will render.

    A template is a folder made of multiple files that would be rendered to create a project.
    """

    path: pathlib.Path
    """The path of the template."""

    files: dict[str, "File"]
    """A dictionnary indicating the files to render."""

    state: TemplateState
    """The actual state of the template."""

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.state = "pending"

    @property
    def has_forge_file(self) -> bool:
        """Indicates if a "forge.py" file exists in the template."""
        return (self.path / "forge.py").exists()

    @property
    def has_cookiecutter_file(self) -> bool:
        """Indicates if a ``cookiecutter.json`` file exists in the template."""
        return (self.path / "cookiecutter.json").exists()

    @property
    def kind(self) -> typing.Literal["fabricius", "cookiecutter"] | None:
        # sourcery skip: assign-if-exp
        """Determine what kind of template this is.
        Either ``Fabricius`` or ``CookieCutter``, or ``None`` if not supported.
        """
        if self.has_forge_file:
            return "fabricius"
        if self.has_cookiecutter_file:
            return "cookiecutter"
        return None

    def with_renderer(self) -> typing.Self:
        # TODO: To be defined
        return self
