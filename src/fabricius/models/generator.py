import copy
import pathlib
from typing import Self

from fabricius.models.file import File, FileCommitResult
from fabricius.signals import after_generator_start, before_generator_start
from fabricius.types import PathLike


class Generator:
    files: list[File]
    """
    The list of files to generate with the generator.
    """

    results: dict[File, FileCommitResult | None] = {}
    """
    The result of each file commit.
    """

    _default_destination: pathlib.Path | None = None
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

    def fake(self) -> Self:
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

    def restore(self) -> Self:
        """
        Tell the generator to generate files upon execution.
        Used for testing purposes.
        """
        self._fake = False
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

    def with_destination(self, path: PathLike) -> Self:
        self._default_destination = pathlib.Path(path)
        return self

    def atomic(self):
        self._atomic = True
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
                if not self._atomic:
                    raise exception
                for file in self.results:
                    file.compute_destination().unlink()

        results = copy.copy(self.results)

        for file in self.files:
            if file not in results.keys():
                results[file] = None

        after_generator_start.send(self)
        return results
