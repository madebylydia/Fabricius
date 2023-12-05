import copy
import pathlib
from fabricius.utils import force_rm
import typing
from fabricius import exceptions
from fabricius.composers import PythonFormatComposer
from fabricius.models.composer import Composer

from fabricius.models.file import File, FileCommitResult
from fabricius.signals import after_generator_start, before_generator_start
from fabricius.types import Data, PathLike


class Generator:
    files: list[File]
    """
    The list of files to generate with the generator.
    """

    data: Data
    """
    The data to pass to the files at generation.
    """

    composer: type[Composer]
    """
    The composer to use to render the files.
    """

    results: dict[File, FileCommitResult | None] = {}
    """
    The result of each file commit.
    """

    base_folder: pathlib.Path | None = None
    """
    A path indicating the default destination for a newly created File instance.
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

    def __init__(self) -> None:
        self.files = []
        self.composer = PythonFormatComposer
        self._atomic = False
        self._fake = False
        super().__init__()

    def _execute_file(self, file: File, allow_overwrite: bool) -> FileCommitResult | None:
        """
        Attempt to commit a file and return its result.
        """
        if self._fake:
            file.fake()

        try:
            file_result = file.commit(overwrite=allow_overwrite)
        except FileExistsError:
            file_result = None
        return file_result

    def fake(self) -> typing.Self:
        """
        Tell the generator to not generate files upon execution.
        Used for testing purposes.

        .. warning::
           Plugins you connect will not directly know that you've been faking file's
           generation, they will get the file's result as if it were correctly saved
           onto the disk. This might create unexpected exceptions.
        """
        self._fake = True
        return self

    def restore(self) -> typing.Self:
        """
        Tell the generator to generate files upon execution.
        Used for testing purposes.
        """
        self._fake = False
        return self

    def to_directory(self, directory: PathLike, *, allow_not_empty: bool = False) -> typing.Self:
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            raise exceptions.ExpectationFailedException(f"Path {path} is not a directory.")
        if not allow_not_empty and path.exists() and not path.iterdir():
            raise exceptions.ExpectationFailedException(f"Directory {path} is not empty.")
        return self

    def with_data(self, data: Data):
        self.data = data
        return self

    def use_composer(self, composer: type[Composer]):
        self.composer = composer
        return self

    def add_file(self, name: str, extension: str | None = None) -> File:
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
        file = File(name, extension)
        if self._default_destination:
            file.to_directory(self._default_destination)
        self.files.append(file)
        return file

    def with_destination(self, path: PathLike) -> typing.Self:
        self._default_destination = pathlib.Path(path)
        return self

    def atomic(self, value: bool):
        self._atomic = value
        return self

    def execute(self, *, allow_overwrite: bool = False) -> dict[File, FileCommitResult | None]:
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
        before_generator_start.send(self)

        for file in self.files:
            try:
                if result := self._execute_file(file, allow_overwrite):
                    self.results[file] = result
            except Exception as exception:
                if self._atomic:
                    for existing_file in self.results:
                        existing_file.compute_destination().unlink()
                raise exception
                # NOTE: Something feels off here.

        results = copy.copy(self.results)

        for file in self.files:
            if file not in results.keys():
                results[file] = None

        after_generator_start.send(self)
        return results

    def _cleanup_rmdir(self):
        """
        Do a cleanup by attempting removing the directory.

        .. warning::

           This is a destructive action, all files will be deleted in this directory.
           May God bless us and hope nothing bad happens here.
        """
        if not self.base_folder:
            raise exceptions.PreconditionException(self, "No base folder set.")
        if not self.base_folder.exists():
            error = FileNotFoundError(f"Directory {self.base_folder.resolve()} does not exist.")
            error.filename = self.base_folder
            raise error
        force_rm(self.base_folder)

    def _cleanup_unlink(self) -> None:
        """
        Do a cleanup by removing all committed file.
        """
        for file in [file for file in self.files if file.state == "persisted"]:
            file.delete()

    def cleanup(self, method: typing.Literal["rmdir", "unlink"] | None = None):
        """
        Cleanup the destination folder. Either remove the folder and its content or committed
        linked to this generator.

        **Methods**

        rmdir :
            Cleanup the generator by removing the folder and its content.

            .. warning:: This will remove ALL content present in this folder, thus, you should
               rather prefer using the unlink method.

        unlink :
            Cleanup the generator by removing files that have been committed.

        Parameters
        ----------
        method : str, either ``rmdir`` or ``unlink``, optional
            The method to use, see explanations above.
            If omitted, ``rmdir`` will be used if :py:attr:`.was_folder_existing_before` is
            ``True`` and ``unlink`` if ``False``.
        """
        if self._atomic:
            match method:
                case "rmdir":
                    self._cleanup_rmdir()
                case "unlink":
                    self._cleanup_unlink()
                case None:
                    self._cleanup_unlink()
            self.state = "deleted"
        else:
            for file in [file for file in self.files if file.state == "persisted"]:
                file.delete()
