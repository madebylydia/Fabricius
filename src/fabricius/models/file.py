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
from fabricius.exceptions import PreconditionException
from fabricius.exceptions.file_commit_exception import ErrorReason, FileCommitException
from fabricius.models.composer import Composer
from fabricius.signals import (
    after_file_commit,
    before_file_commit,
    on_file_commit_fail,
    on_file_deleted,
)
from fabricius.types import MutableData, PathLike

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

    data: MutableData
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

    composer: Composer
    """
    The composer to use to generate the file.
    """

    data: MutableData
    """
    The data that will be passed to the composer.
    """

    will_fake: bool
    """
    If the file should fake its creation upon commit.
    """

    should_overwrite: bool
    """
    If the file should overwrite an existing file upon commit.
    """

    def __init__(self, name: str, extension: str | None = None) -> None:
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
        self.will_fake = False
        self.should_overwrite = False

        self.composer = PythonFormatComposer()
        self.data = {}

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
        :py:class:`pathlib.Path` :
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

    def to_directory(self, directory: PathLike) -> Self:
        """
        Set the directory where the file will be saved.

        .. warning ::
           If a file already exist at this location, it will raise an exception if you do not
           allow for :py:meth:`.overwrite` first.

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            Where the file will be stored. Does not include the file's name.

        Raises
        ------
        :py:exc:`NotADirectoryError` :
            The given path exists but is not a directory.
        """
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            error = NotADirectoryError(f"{path} is not a directory.")
            error.filename = path
            raise error
        self.destination = path
        return self

    def use_mustache(self) -> Self:
        """
        Use chevron (Mustache) to render the template.
        """
        self.composer = ChevronComposer()
        return self

    def use_string_template(self) -> Self:
        """
        Use string.Template to render the template.
        """
        self.composer = StringTemplateComposer()
        return self

    def use_jinja(self) -> Self:
        """
        Use Jinja2 to render the template.
        """
        self.composer = JinjaComposer()
        return self

    def with_composer(self, composer: Composer) -> Self:
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

    def with_data(self, data: MutableData, *, overwrite: bool = True) -> Self:
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
            self.data = {}
        self.data.update(data)
        return self

    def overwrite(self, should_overwrite: bool) -> Self:
        """
        Set the file to overwrite or not.
        This will overwrite any existing file that might be already be on the disk.

        Parameters
        ----------
        should_overwrite : :py:class:`bool`
            The value to set the overwrite parameter to.
        """
        self.should_overwrite = should_overwrite
        return self

    def fake(self, should_fake: bool) -> Self:
        """
        Set the file to fake the commit.
        This will ensure that the file does not get stored on the machine upon commit.

        .. warning::
           Plugins you connect will not directly know that you've been faking file's
           generation, they will get the file's result as if it were correctly saved
           onto the disk. This might create unexpected exceptions.

        Parameters
        ----------
        should_fake : :py:class:`bool`
            The value to set the fake parameter to.
        """
        self.will_fake = should_fake
        return self

    def generate(self) -> str:
        """
        Generate the file's content.
        This method does not store the file on the disk, but just generate the final content. You
        should use :py:meth:`.commit` to save the file permanently.

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

        return self.composer.push_data(self.data).render(self.content)

    def commit(self) -> FileCommitResult:
        """
        Save the file to the disk.

        Raises
        ------
        :py:exc:`fabricius.exceptions.PreconditionException` :
            If a required value was not set. (Content or destination)
        :py:exc:`fabricius.exceptions.FileCommitException` :
            If the file has already been persisted, deleted, or being persisted.
        :py:exc:`FileExistsError` :
            If the file already exists on the disk and the file is not set to overwrite.

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
        if self.state == "processing":
            raise FileCommitException(self, ErrorReason.IS_PENDING)
        if self.state == "persisted":
            raise FileCommitException(self, ErrorReason.ALREADY_PERSISTED)
        if self.state == "deleted":
            raise FileCommitException(self, ErrorReason.ALREADY_DELETED)
        if self.state == "failed":
            raise FileCommitException(self, ErrorReason.FAILED)

        destination = self.compute_destination()

        if destination.exists() and not self.should_overwrite:
            exception = FileExistsError(f"File '{self.name}' already exists.")
            exception.filename = self.name
            raise exception

        self.state = "processing"

        final_content = self.generate()

        try:
            before_file_commit.send(self)

            if self.will_fake:
                self.state = "persisted"
            else:
                with contextlib.suppress(NotADirectoryError):
                    if not destination.parent.exists():
                        destination.parent.mkdir(parents=True)
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
            fake=self.will_fake,
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
        on_file_deleted.send(self)
