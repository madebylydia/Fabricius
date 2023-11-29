import contextlib
import pathlib
import typing

from typing_extensions import Self

from fabricius.composers import (
    ChevronComposer,
    JinjaComposer,
    PythonFormatComposer,
    StringTemplateComposer,
)
from fabricius.exceptions import ExpectationFailedException, PreconditionException
from fabricius.exceptions.file_commit_exception import ErrorReason, FileCommitException
from fabricius.models.composer import Composer
from fabricius.signals import after_file_commit, before_file_commit, on_file_commit_fail
from fabricius.types import Data, PathLike

FILE_STATE: typing.TypeAlias = typing.Literal[
    "pending", "processing", "failed", "persisted", "deleted"
]


class FileCommitResult(typing.TypedDict):
    """
    A FileCommitResult is returned when a file was successfully saved.
    It returns its information after its creation.
    """

    name: str
    """
    The name of the file.
    """

    state: FILE_STATE
    """
    The state of the file. Should always be "persisted".
    """

    destination: pathlib.Path
    """
    Where the file is located/has been saved.
    """

    data: Data
    """
    The data that has been passed during rendering.
    """

    template_content: str
    """
    The original content of the template.
    """

    content: str
    """
    The resulting content of the saved file.
    """

    fake: bool
    """
    If the file was faked.
    If faked, the file has not been saved to the disk.
    """


class File:
    """
    The builder class to initialize a file template.
    The result (Through the :py:meth:`.generate` method) is the render of the file's content.
    You can "commit" the file to the disk to persist the file's content.
    """

    name: str
    """
    The name of the file that will be generated.
    """

    state: FILE_STATE
    """
    The state of the file.
    """

    content: str | None
    """
    The template's content.
    """

    destination: pathlib.Path | None
    """
    The destination of the file, if set.
    """

    composer: type[Composer]
    """
    The composer to use to generate the file.
    """

    data: Data
    """
    The data that will be passed to the composer.
    """

    _will_fake: bool
    """
    If the file should fake its creation upon commit.
    """

    def __init__(self, name: str, extension: typing.Optional[str] = None) -> None:
        """
        Parameters
        ----------
        name : :py:class:`str`
            The name of the file.
        extension : :py:class:`str`
            The extension of the file, without dot, same as ``name="<name>.<extension>"`` (Where
            ``<name>`` and ``<extensions>`` are the arguments given to the class).
        """
        self.name = f"{name}.{extension}" if extension else name
        self.state = "pending"
        self.content = None
        self.destination = None
        self._will_fake = False

        self.composer = PythonFormatComposer
        self.data = Data({})

    def compute_destination(self) -> pathlib.Path:
        """
        Compute the destination of the file.

        Raises
        ------
        :py:exc:`fabricius.exceptions.PreconditionException` :
            If the object does not have the property "destination" set.
            (Use :py:meth:`.to_directory`)

        Returns
        -------
        pathlib.Path :
            The final path.
        """
        if not self.destination:
            raise PreconditionException(self, "destination property must be set.")

        return (self.destination / self.name).resolve()

    def from_file(self, path: str | pathlib.Path) -> Self:
        """
        Read the content from a file template.

        Raises
        ------
        :py:exc:`FileNotFoundError` :
            If the file was not found.

        Parameters
        ----------
        path : :py:class:`str` or :py:class:`pathlib.Path`
            The path of the file template.
        """
        path = pathlib.Path(path).resolve()
        self.content = path.read_text()
        return self

    def from_content(self, content: str) -> Self:
        """
        Read the content from a string.

        Parameters
        ----------
        content : :py:class:`str`
            The template you want to format.
        """
        self.content = content
        return self

    def to_directory(self, directory: PathLike, *, allow_not_empty: bool = False) -> Self:
        """
        Set the directory where the file will be saved.

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            Where the file will be stored. Does not include the file's name.

        allow_not_empty : :py:class:`bool`
            If the directory is not empty, :py:exc:`ExpectationFailedException` will be raised if
            set to ``False``.

        Raises
        ------
        :py:exc:`ExpectationFailedException` :
            The given path exists but is not a directory.
            OR
            The given path is not empty and ``allow_not_empty`` is set to ``False``.
        """
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            raise ExpectationFailedException(f"{path} is not a directory.")
        if path.exists() and not path.iterdir() and not allow_not_empty:
            raise ExpectationFailedException(f"{path} contains files.")
        self.destination = path
        return self

    def use_mustache(self) -> Self:
        """
        Use chevron (Mustache) to render the template.
        """
        self.composer = ChevronComposer
        return self

    def use_string_template(self) -> Self:
        """
        Use string.Template to render the template.
        """
        self.composer = StringTemplateComposer
        return self

    def use_jinja(self) -> Self:
        """
        Use Jinja2 to render the template.
        """
        self.composer = JinjaComposer
        return self

    def with_composer(self, composer: typing.Type[Composer]) -> Self:
        """
        Use a custom composer to render the template.

        Parameters
        ----------
        composer : Type of :py:class:`fabricius.models.composer.Composer`
            The composer to use to format the file.
            It must be not initialized.
        """
        self.composer = composer
        return self

    def with_data(self, data: Data, *, overwrite: bool = True) -> Self:
        """
        Add data to pass to the template.

        Parameters
        ----------
        data : :py:const:`fabricius.types.Data`
            The data you want to pass to the template.
        overwrite : :py:class:`bool`
            If the data that already exists should be deleted. If False, the new data will be
            added on top of the already existing data. Default to ``True``.
        """
        if overwrite:
            self.data = Data({})
        self.data.update(data)
        return self

    def fake(self) -> Self:
        """
        Set the file to fake the commit.
        This will ensure that the file does not get stored on the machine upon commit.
        """
        self._will_fake = True
        return self

    def restore(self) -> Self:
        """
        Set the file to not fake the commit.
        This will ensure that the file gets stored on the machine upon commit.

        .. hint ::

           This is the default behavior. It's only useful to use this method if you have used
           :py:meth:`.fake`.
        """
        self._will_fake = False
        return self

    def generate(self) -> str:
        """
        Generate the file's content.

        Raises
        ------
        :py:exc:`fabricius.exceptions.PreconditionException` :
            If no content to the file were added.

        Returns
        -------
        :py:class:`str` :
            The final content of the file.
        """
        if not self.content:
            raise PreconditionException(self, "content must be set")

        return self.composer(self.data).render(self.content)

    def commit(self, *, overwrite: bool = False) -> FileCommitResult:
        """
        Save the file to the disk.

        Parameters
        ----------
        overwrite : :py:class:`bool`
            If a file exist at the given path, shall the overwrite parameter say if the file
            should be overwritten or not. Default to ``False``.

        Raises
        ------
        :py:exc:`fabricius.exceptions.PreconditionException` :
            If a required value was not set. (Content or destination)
        :py:exc:`fabricius.exceptions.FileCommitException` :
            If the file has already been saved to the disk.
        :py:exc:`FileExistsError` :
            If the file already exists on the disk and ``overwrite`` is set to ``False``.

            This is different from
            :py:exc:`AlreadyCommittedError <fabricius.exceptions.AlreadyCommittedError>`
            because this indicates that the content of the file this generator was never actually
            saved.
        :py:exc:`OSError` :
            The file's name is not valid for the OS.

        Returns
        -------
        :py:class:`fabricius.types.FileCommitResult` :
            A typed dict with information about the created file.
        """
        if not self.destination:
            raise PreconditionException(self, "destination must be set.")
        if not self.content:
            raise PreconditionException(self, "content must be set.")
        if self.state == "persisted":
            raise FileCommitException(self, ErrorReason.ALREADY_PERSISTED)

        destination = self.compute_destination()

        if destination.exists() and not overwrite:
            exception = FileExistsError(f"File '{self.name}' already exists.")
            exception.filename = self.name
            raise exception

        self.state = "processing"

        before_file_commit.send(self)
        final_content = self.generate()

        try:
            if self._will_fake:
                self.state = "persisted"
            else:
                with contextlib.suppress(NotADirectoryError):
                    if not destination.parent.exists():
                        destination.parent.mkdir()
                    destination.write_text(final_content)
                    self.state = "persisted"
        except Exception as exception:
            self.state = "failed"
            on_file_commit_fail.send(self)

        commit = FileCommitResult(
            name=self.name,
            state=self.state,
            data=self.data,
            template_content=self.content,
            content=final_content,
            destination=self.destination / self.name,
            fake=self._will_fake,
        )

        after_file_commit.send(self, commit)
        return commit

    def delete(self) -> None:
        """
        Delete the file if persisted.
        """
        if not self.compute_destination().exists():
            error = FileNotFoundError(f"Cannot delete {self.name}: File does not exist on disk.")
            error.filename = self.compute_destination()
            raise error
        self.compute_destination().unlink()
        self.state = "deleted"
