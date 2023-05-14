import pathlib
import typing

from typing_extensions import Self

from fabricius.app.signals import after_template_commit, before_template_commit
from fabricius.exceptions import (
    AlreadyCommittedError,
    ConflictError,
    MissingRequiredValueError,
)
from fabricius.models.file import File, FileCommitResult
from fabricius.models.renderer import Renderer
from fabricius.types import Data, PathStrOrPath

STATE = typing.Literal["pending", "failed", "persisted"]
RendererType = typing.TypeVar("RendererType", bound=type[Renderer])


class Template(typing.Generic[RendererType]):
    state: STATE

    base_folder: pathlib.Path

    files: list[File]

    data: Data

    renderer: RendererType

    _will_fake: bool

    def __init__(
        self,
        base_folder: PathStrOrPath,
        renderer: RendererType,
    ) -> None:
        self.base_folder = pathlib.Path(base_folder)
        self.state = "pending"
        self.files = []
        self.data = {}
        self.renderer = renderer
        self._will_fake = False

    @property
    def __files_destinations(self) -> list[pathlib.Path | None]:
        return [file.destination for file in self.files]

    def add_file(self, file: File) -> Self:
        if not file.can_commit:
            reason = file.can_commit
            if reason == "state":
                raise AlreadyCommittedError(file.name)
            raise MissingRequiredValueError(self, reason)

        if file.destination and file.compute_destination() in self.__files_destinations:
            raise ConflictError(
                file,
                f"File {file.name} has a destination that already is present in Template's destinations.",
            )

        self.files.append(file)
        return self

    def add_files(self, files: typing.Iterable[File]) -> Self:
        for file in files:
            self.add_file(file)
        return self

    def push_data(self, data: Data) -> Self:
        self.data = data
        return self

    def fake(self) -> Self:
        self._will_fake = True
        return self

    def restore(self) -> Self:
        self._will_fake = False
        return self

    def commit(self) -> list[FileCommitResult]:
        results: list[FileCommitResult] = []

        before_template_commit.send(self)

        for file in self.files:
            file.with_data(self.data, overwrite=False)
            if self._will_fake:
                file.fake()
            else:
                # Just in case they've been set to fake...
                file.restore()
            result = file.commit()
            results.append(result)

        after_template_commit.send(self, results)

        return results
