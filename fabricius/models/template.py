import pathlib
import typing
from shutil import rmtree

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

STATE = typing.Literal["pending", "failed", "persisted", "deleted"]
RendererType = typing.TypeVar("RendererType", bound=type[Renderer])


class Template(typing.Generic[RendererType]):
    """
    The :py:class:`Template` class represent "a collection of files that, in its whole, represents
    a project"

    The difference between the :py:class:`.Template` class and a collection of :py:class:`.File`
    is that a template assumes all of your files have the same properties. (Requires the same
    renderer, the same data, etc.)

    Typically, a template only use one renderer, and shares the same data across the whole project
    template.

    The :py:class:`.Template` will assist creating a project, while providing a similar interface
    of the :py:class:`.File` model.
    """

    state: STATE
    """
    The state of the template
    """

    base_folder: pathlib.Path
    """
    The folder where the template will be generated.
    """

    files: list[File]
    """
    The list of files that will be rendered when committing.
    """

    data: Data
    """
    The data to pass to the files.
    """

    renderer: RendererType
    """
    The renderer that will be used to generate the files.
    """

    was_folder_existing_before: bool
    """
    Indicate if the folder was existing before creating the template.
    Useful to know if the folder should be removed instead of removing each files.
    """

    _will_fake: bool

    def __init__(
        self,
        base_folder: PathStrOrPath,
        renderer: RendererType,
    ) -> None:
        """
        Parameters
        ----------
        base_folder : :py:const:`fabricius.types.PathStrOrPath`
            Indication of where the template should be generated.
        renderer : Type of :py:class:`fabricius.models.renderer.Renderer`
            The renderer to use with the template.
        """
        self.base_folder = pathlib.Path(base_folder)
        self.state = "pending"
        self.files = []
        self.data = {}
        self.renderer = renderer
        self.was_folder_existing_before = self.base_folder.exists()
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

    def commit(self, *, overwrite: bool = False) -> list[FileCommitResult]:
        results: list[FileCommitResult] = []

        before_template_commit.send(self)

        for file in self.files:
            file.with_data(self.data, overwrite=False)
            if self._will_fake:
                file.fake()
            else:
                # Just in case they've been set to fake...
                file.restore()

            result = file.commit(overwrite=overwrite)
            results.append(result)

        after_template_commit.send(self, results)

        return results

    def _cleanup_rmdir(self):
        """
        Do a cleanup by attempting removing the directory.
        """
        if not self.base_folder.exists():
            error = FileNotFoundError(f"Directory {self.base_folder.resolve()} does not exist.")
            error.filename = self.base_folder
            raise error
        rmtree(self.base_folder)

    def _cleanup_unlink(self) -> None:
        """
        Do a cleanup by removing all committed file.
        """
        for file in [file for file in self.files if file.state == "persisted"]:
            file.delete()

    def cleanup(self, method: typing.Literal["rmdir", "unlink"] | None = None):
        """
        Cleanup the destination folder. Either remove the folder and its content or committed
        linked to this template.

        **Methods**

        rmdir :
            Cleanup the template by removing the folder and its content.

            .. warning:: This will remove ALL content present in this folder, thus, you should
               rather prefer using the unlink method.

        unlink :
            Cleanup the template by removing files that have been committed.

        Parameters
        ----------
        method : str, either ``rmdir`` or ``unlink``, optional
            The method to use, see explanations above.
            If omitted, ``rmdir`` will be used if :py:attr:`.was_folder_existing_before` is
            ``True`` and ``unlink`` if ``False``.
        """
        match method:
            case "rmdir":
                self._cleanup_rmdir()
            case "unlink":
                self._cleanup_unlink()
            case None:
                if self.was_folder_existing_before:
                    self._cleanup_unlink()
                else:
                    self._cleanup_rmdir()
        self.state = "deleted"
