import pathlib
import typing

from fabricius.models.file import File

PROJECT_STATE: typing.TypeAlias = typing.Literal["pending", "processing", "failed", "persisted"]


class Project:
    """
    Class that represent a project that will be rendered from a
    :py:class:`fabricius.models.library.Library`.
    """

    destination: pathlib.Path

    state: PROJECT_STATE

    _files: list[File]

    _will_fake: bool

    def add_file(self, file: File):
        self._files.append(file)
        return self

    def generate(self) -> None:
        pass
