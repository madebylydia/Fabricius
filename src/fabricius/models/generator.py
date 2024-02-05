import logging
import pathlib
import typing

from fabricius import exceptions
from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.models.file import File, FileCommitResult
from fabricius.signals import after_generator_start, before_generator_start
from fabricius.types import Data, PathLike
from fabricius.utils import contains_files, force_rm

if typing.TYPE_CHECKING:
    import collections.abc

    from fabricius.models.composer import Composer

_log = logging.getLogger(__name__)


class GeneratorExecutionResult(typing.TypedDict):
    """The result of a generator execution."""

    files: list[File]
    """The file that was generated."""

    base_folder: pathlib.Path
    """The base folder where the files were generated."""

    data: Data
    """The data that was passed to files."""


class Generator[ComposerType: "Composer"]:
    """The Generator class represents a file generator that is responsible for generating files
    based on a set of templates and data.

    This is used to generate multiple files that share the same settings all together.
    """

    files: list[File]
    """The list of files to generate with the generator."""

    destination: pathlib.Path | None = None
    """A path indicating the default destination for a newly created File instance."""

    composer: ComposerType
    """The composer to use to render the files."""

    data: Data
    """The data to pass to the files at generation."""

    is_atomic: bool
    """Define the generator as atomic.
    Means that if one file fails, the whole generator will fail and committed files will be
    deleted.
    """

    should_fake: bool
    """If the generator should create the files or not."""

    should_overwrite: bool
    """If the generator should overwrite existing files or not."""

    def __init__(self, composer: ComposerType) -> None:
        self.files = []
        self.composer = composer
        self.destination = None
        self.is_atomic = False
        self.should_fake = False
        self.should_overwrite = False
        super().__init__()

    def _prepare_file(self, file: File) -> None:
        if not self.destination:
            raise exceptions.PreconditionException(self, "destination must be set")
        if not file.destination:
            file.to_directory(self.destination)
        file.with_data(self.data)
        file.with_composer(self.composer)
        file.fake(self.should_fake)
        file.overwrite(self.should_overwrite)

    def fake(self, should_fake: bool) -> typing.Self:
        """Set the generator to fake the execution.
        In other words, not generate the files it receives.

        .. warning::
           Plugins you connect will not directly know that you've been faking file's
           generation, they will get the file's result as if it were correctly saved
           onto the disk. This might create unexpected exceptions.

        Parameters
        ----------
        should_fake : :py:class:`bool`
            The value to set the generator to.
        """
        self.should_fake = should_fake
        return self

    def overwrite(self, should_overwrite: bool) -> typing.Self:
        """Set the generator to overwrite files that already exist.

        Parameters
        ----------
        should_overwrite : :py:class:`bool`
            The value to set the generator to.
        """
        self.should_overwrite = should_overwrite
        return self

    def to_directory(self, directory: PathLike) -> typing.Self:
        """Indicate the directory where the files will be generated.

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            The directory where the files will be generated.
        """
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            raise exceptions.PreconditionException(self, f"Path {path} is not a directory.")
        self.destination = path
        return self

    def with_data(self, data: Data):
        """Set data to pass to the generator.

        Parameters
        ----------
        data : :py:const:`fabricius.types.Data`
            The data you want to pass to the generator.
        """
        self.data = data
        return self

    def add_file(self, file: File) -> File:
        """Add a file to the generator.

        Parameters
        ----------
        file : :py:class:`fabricius.models.File`
            The file to append to this generator.

        Returns
        -------
        :py:class:`fabricius.file.File` :
            The same file.
        """
        _log.debug("[Generator id=%s] Adding %s", id(self), file)
        self.files.append(file)
        return file

    def add_files(self, *files: File) -> typing.Self:
        """Add multiple files to the generator.

        Parameters
        ----------
        files : :py:class:`fabricius.file.File`
            The files to add to the generator.
        """
        for file in files:
            self.files.append(file)
        return self

    def atomic(self, value: bool):
        """Define the generator as atomic.
        This means that if one file fails, the whole generator will fail and committed files will
        be deleted.

        Parameters
        ----------
        value : :py:class:`bool`
            If the generator should be atomic or not.
        """
        self.is_atomic = value
        return self

    def execute(self) -> GeneratorExecutionResult:
        """Execute generator's tasks.

        Raises
        ------
        :py:class:`fabricius.exceptions.PreconditionException` :
            This error will be raised if the destination is not set.
            It can also be raised if the destination is not empty and that overwriting is not
            allowed.
        :py:class:`Exception` :
            Any exception raised by a file during its commit.

        Returns
        -------
        Dict[:py:class:`fabricius.file.File`, :py:class:`fabricius.file.FileCommitResult`] :
            A dict containing a file generator and its commit result.
            In case the value is ``None``, this mean that the file was not successfully saved to
            the disk (Already committed, file already exists, etc.).
        """
        if not self.destination:
            raise PreconditionException(self, "destination must be set")
        if not self.should_overwrite and contains_files(self.destination):
            raise exceptions.PreconditionException(
                self, f"Directory {self.destination} is not empty and overwrite is not allowed."
            )

        before_generator_start.send(self)

        has_generation_failed: (
            tuple[typing.Literal[False], None] | tuple[typing.Literal[True], Exception]
        ) = (False, None)
        results: dict[File, FileCommitResult] = {}

        for file in self.files:
            try:
                self._prepare_file(file)
                result = file.commit()
                results[file] = result
            except Exception as exception:
                has_generation_failed = True, exception
                break

        # Don't remove the "is True", it's used for the the 2nd item in the tuple, which wouldn't
        # be checked correctly otherwise
        if has_generation_failed[0] is True:
            if self.is_atomic:
                self.cleanup("unlink")
            raise has_generation_failed[1]

        after_generator_start.send(self)
        return GeneratorExecutionResult(
            files=self.files,
            base_folder=self.destination,
            data=self.data,
        )

    def _cleanup_rmdir(self):
        """Do a cleanup by attempting removing the directory.

        .. warning::

           This is a destructive action, all files will be deleted in this directory.
           May God bless us and hope nothing bad happens here.
        """
        if not self.destination:
            raise exceptions.PreconditionException(self, "No base folder set.")
        force_rm(self.destination)

    def _cleanup_unlink(self, files: "collections.abc.Iterable[File]") -> None:
        """Do a cleanup by removing all committed file.

        Parameters
        ----------
        files : Optional, :py:class:`list` of :py:class:`fabricius.file.File`
            The files to cleanup. If ``None``, all files that have been persisted will be removed.
        """
        for file in [file for file in files if file.state == "persisted"]:
            file.delete()

    def cleanup(
        self,
        method: typing.Literal["rmdir", "unlink"] | None = None,
    ) -> None:
        """Cleanup the destination folder. Either remove the folder and its content or committed
        linked to this generator.

        **Methods**

        unlink :
            Cleanup the generator by removing files that have been committed.

        rmdir :
            Cleanup the generator by removing the folder and its content.

            .. warning:: This will remove ALL content present in this folder, thus, you should
               rather prefer using the unlink method.

        Parameters
        ----------
        method : Optional :py:class:`str`, either ``rmdir`` or ``unlink``
            The method to use, see explanations above.
            If omitted, all files that have been persisted will be removed.
        """
        match method:
            case "rmdir":
                self._cleanup_rmdir()
            case "unlink":
                self._cleanup_unlink(self.files)
            case None:
                for file in [file for file in self.files if file.state == "persisted"]:
                    file.delete()
