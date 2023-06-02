import pathlib
import typing


class Template:
    """
    The template class represent the base of an application.
    This is what Fabricius will render.

    A template is a folder made of multiple files that would be rendered to create a project.
    """

    path: pathlib.Path
    """
    The path of the template.
    """

    _kind: typing.Literal["fabricius", "cookiecutter"] | None

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self._kind = None

    @property
    def has_forge_file(self) -> bool:
        """
        Indicates if a "forge.py" file exists in the template.

        Returns
        -------
        bool
            If a ``forge.py`` file exist.
        """
        return self.path.joinpath("forge.py").exists()

    @property
    def has_cookiecutter_file(self) -> bool:
        """
        Indicates if a ``cookiecutter.json`` file exists in the template.

        Returns
        -------
        bool
            If a ``cookiecutter.json`` file exist.
        """
        return self.path.joinpath("cookiecutter.json").exists()

    @property
    def kind(self) -> typing.Literal["fabricius", "cookiecutter"] | None:
        """
        Determine what kind of template this is.
        Either ``Fabricius`` or ``CookieCutter``, or ``None`` if not supported.
        """
        if self._kind:
            return self._kind

        if self.has_forge_file:
            self._kind = "fabricius"
        if self.has_cookiecutter_file:
            self._kind = "cookiecutter"

        return self._kind
