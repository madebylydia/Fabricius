import pathlib
import typing

from fabricius import exceptions
from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.models.composer import Composer
from fabricius.models.file import File, FileCommitResult
from fabricius.signals import after_generator_start, before_generator_start
from fabricius.types import MutableData, PathLike
from fabricius.utils import contains_files, force_rm

# TODO: Rewrite this class. It's being heavily reworked.


class GeneratorExecutionResult(typing.TypedDict):
    """
    The result of a generator execution.
    """

    files: list[File]
    """
    The file that was generated.
    """

    base_folder: pathlib.Path
    """
    The base folder where the files were generated.
    """

    data: MutableData
    """
    The data that was passed to files.
    """


class Generator[ComposerType: Composer]:
    """
    The Generator class represents a file generator that is responsible for generating files
    based on a set of templates and data.

    This is used to generate multiple files that share the same settings all together.
    """

    files: list[File]
    """
    The list of files to generate with the generator.
    """

    destination: pathlib.Path | None = None
    """
    A path indicating the default destination for a newly created File instance.
    """

    composer: ComposerType
    """
    The composer to use to render the files.
    """

    data: MutableData
    """
    The data to pass to the files at generation.
    """

    _atomic: bool
    """
    Define the generator as atomic.
    Means that if one file fails, the whole generator will fail and committed files will be
    deleted.
    """

    _fake: bool
    """
    If the generator should create the files or not.
    """

    _overwrite: bool
    """
    If the generator should overwrite existing files or not.
    """

    def __init__(self, composer: ComposerType) -> None:
        self.files = []
        self.composer = composer
        self.destination = None
        self._atomic = False
        self._fake = False
        self._overwrite = False
        super().__init__()

    def _prepare_file(self, file: File) -> None:
        if not self.destination:
            raise exceptions.PreconditionException(self, "destination must be set")
        if not file.destination:
            file.to_directory(self.destination)
        file.with_data(self.data)
        file.with_composer(self.composer)
        file.fake(self._fake)
        file.overwrite(self._overwrite)

    def fake(self, should_fake: bool) -> typing.Self:
        """
        Set the generator to fake the execution.
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
        self._fake = should_fake
        return self

    def to_directory(self, directory: PathLike, *, allow_not_empty: bool = False) -> typing.Self:
        """
        Indicate the directory where the files will be generated.

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            The directory where the files will be generated.
        allow_not_empty : :py:class:`bool`
            If the directory is not empty, shall the generator still generate files or not.
            If ``False``, an exception will be raised.
        """
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            raise exceptions.ExpectationFailedException(f"Path {path} is not a directory.")
        if not allow_not_empty and path.exists() and contains_files(path):
            raise exceptions.ExpectationFailedException(f"Directory {path} is not empty.")
        self.destination = path
        return self

    def with_data(self, data: MutableData):
        """
        Set data to pass to the generator.

        Parameters
        ----------
        data : :py:const:`fabricius.types.Data`
            The data you want to pass to the generator.
        """
        self.data = data
        return self

    def add_file(self, file: File) -> File:
        """
        Add a file to the generator.

        Parameters
        ----------
        name : :py:class:`str`
            The name of the file
        extension : Optional, :py:class:`str`
            The extension of the file, can be optional.
            If none, no extension will be added.

        Returns
        -------
        :py:class:`fabricius.file.File` :
            The generated file. You then have to set file's options.
        """
        self.files.append(file)
        return file

    def add_files(self, *files: File) -> typing.Self:
        """
        Add multiple files to the generator.

        Parameters
        ----------
        files : :py:class:`fabricius.file.File`
            The files to add to the generator.
        """
        for file in files:
            self.files.append(file)
        return self

    def overwrite(self, value: bool) -> typing.Self:
        """
        Set the generator to overwrite files that already exist.

        Parameters
        ----------
        value : :py:class:`bool`
            The value to set the generator to.
        """
        self._overwrite = value
        return self

    def atomic(self, value: bool):
        """
        Define the generator as atomic.
        This means that if one file fails, the whole generator will fail and committed files will
        be deleted.

        Parameters
        ----------
        value : :py:class:`bool`
            If the generator should be atomic or not.
        """
        self._atomic = value
        return self

    def execute(self) -> GeneratorExecutionResult:
        """
        Execute generator's tasks.

        Parameters
        ----------
        allow_overwrite : :py:class:`bool`
            If files exist at their set path, shall this parameter say if files should be
            overwritten or not.

        Returns
        -------
        Dict[:py:class:`fabricius.file.File`, :py:class:`fabricius.file.FileCommitResult`] :
            A dict containing a file generator and its commit result.
            In case the value is ``None``, this mean that the file was not successfully saved to
            the disk (Already committed, file already exists, etc.).
        """
        if not self.destination:
            raise PreconditionException(self, "destination must be set")

        before_generator_start.send(self)

        has_generation_failed: typing.Union[
            tuple[typing.Literal[False], None], tuple[typing.Literal[True], Exception]
        ] = (False, None)
        results: dict[File, FileCommitResult] = {}

        for file in self.files:
            try:
                self._prepare_file(file)
                result = file.commit()
                results[file] = result
            except Exception as exception:
                has_generation_failed = True, exception
                break

        if (
            has_generation_failed[0] is True
        ):  # Don't remove the "is True", it's used for the the 2nd item in the tuple, which wouldn't be checked correctly otherwise
            if self._atomic:
                self.cleanup("unlink", files=results.keys())
            raise has_generation_failed[1]

        after_generator_start.send(self)
        return GeneratorExecutionResult(
            files=self.files,
            base_folder=self.destination,
            data=self.data,
        )

    def _cleanup_rmdir(self):
        """
        Do a cleanup by attempting removing the directory.

        .. warning::

           This is a destructive action, all files will be deleted in this directory.
           May God bless us and hope nothing bad happens here.
        """
        if not self.destination:
            raise exceptions.PreconditionException(self, "No base folder set.")
        force_rm(self.destination)

    def _cleanup_unlink(self, files: typing.Iterable[File] | None = None) -> None:
        """
        Do a cleanup by removing all committed file.

        Parameters
        ----------
        files : Optional, :py:class:`list` of :py:class:`fabricius.file.File`
            The files to cleanup. If ``None``, all files that have been persisted will be removed.
        """
        for file in [file for file in self.files if file.state == "persisted"]:
            file.delete()

    @typing.overload
    def cleanup(
        self,
        method: typing.Literal["rmdir", "unlink"] = "unlink",
        *,
        files: typing.Iterable[File] | None = None,
    ) -> None:
        ...

    @typing.overload
    def cleanup(self, method: typing.Literal["rmdir", "unlink"] | None = None) -> None:
        ...

    def cleanup(
        self,
        method: typing.Literal["rmdir", "unlink"] | None = None,
        *,
        files: typing.Iterable[File] | None = None,
    ) -> None:
        """
        Cleanup the destination folder. Either remove the folder and its content or committed
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
                self._cleanup_unlink(files)
            case None:
                for file in [file for file in self.files if file.state == "persisted"]:
                    file.delete()
