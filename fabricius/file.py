import contextlib
import pathlib
import typing

from typing_extensions import Self

from fabricius.const import FILE_STATE, Data, PathStrOrPath
from fabricius.errors import FabriciusError
from fabricius.renderer import (
    ChevronRenderer,
    PythonFormatRenderer,
    Renderer,
    StringTemplateRenderer,
)


class NoContentError(FabriciusError):
    """
    The file does not have any content.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file does not have any content.
        """
        super().__init__(f"File '{file_name}' was not set with a content/template.")


class NoDestinationError(FabriciusError):
    """
    The file does not know where to go.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file does not know where to go.
        """
        super().__init__(f"File '{file_name}' does not have a destination set.")


class AlreadyCommittedError(FabriciusError):
    """
    The file has already been committed/persisted.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file has already been committed/persisted.
        """
        super().__init__(f"File '{file_name}' has already been committed.")


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


class File:
    """
    The File class helps with creating files from templates by taking the template's path,
    destination's path, the renderer to use, data to include, etc.
    The base of Fabricius, basically.
    """

    name: str
    """
    The name of the file that will be generated.
    """

    state: FILE_STATE
    """
    The state of the file.
    """

    content: typing.Optional[str]
    """
    The template's content.
    """

    template_content: typing.Optional[str]
    """
    The content of the base template, if set.
    """

    destination: typing.Optional[pathlib.Path]
    """
    The destination of the file, if set.
    """

    renderer: typing.Type[Renderer]
    """
    The renderer to use to generate the file.
    """

    data: Data
    """
    The data that will be passed to the renderer.
    """

    will_fake: bool
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
            The extension of the file, without dot, same as ``name="<name>.<extension>"``
        """
        self.name = f"{name}.{extension}" if extension else name
        self.state = "pending"
        self.content = None
        self.destination = None
        self.will_fake = False

        self.renderer = PythonFormatRenderer
        self.data = {}

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

    def to_directory(self, directory: PathStrOrPath) -> Self:
        """
        Set the directory where the file will be saved.

        Raises
        ------
        :py:exc:`NotADirectory` :
            The given path exists but is not a directory.

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            Where the file will be stored. Does not include the file's name.
        """
        path = pathlib.Path(directory).resolve()
        if path.exists() and not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")
        self.destination = path
        return self

    def use_mustache(self) -> Self:
        """
        Use chevron (Mustache) to render the template.
        """
        self.renderer = ChevronRenderer
        return self

    def use_string_template(self) -> Self:
        """
        Use string.Template to render the template.
        """
        self.renderer = StringTemplateRenderer
        return self

    def with_renderer(self, renderer: typing.Type[Renderer]) -> Self:
        """
        Use a custom renderer to render the template.

        Parameters
        ----------
        renderer : Type of :py:class:`fabricius.renderer.Renderer`
            The renderer to use to format the file.
            It must be not initialized.
        """
        self.renderer = renderer
        return self

    def with_data(self, data: Data, *, overwrite: bool = True, automatic_str: bool = True) -> Self:
        """
        Add data to pass to the template.

        .. note :: Elements of the data you've passed will be automatically converted to str as to
            not render incorrectly in the template (For example,
            ``datetime.datetime(2023, 2, 23, 17, 39, 5, 128944)`` instead of
            ``2023-02-23 17:39:05.128944``), if you wish to disable this feature, use the
            ``automatic_str`` keyword parameter.
            This process is done before the data is registered to the class.

        Parameters
        ----------
        data : :py:data:`fabricius.const.Data`
            The data you want to pass to the template.
        overwrite : :py:class:`bool`
            If the data that already exists should be deleted. If False, the new data will be
            added on top of the already existing data. Default to ``True``.
        automatic_str : :py:class:`bool`
            When passing data, all elements will be automatically converted to :py:class:`str`, as
            to render each element correctly in the template, and not Python's representation of
            the elements.
        """
        if overwrite:
            self.data = {}
        if automatic_str:
            for key, value in data.items():
                data[key] = str(value)
        self.data.update(data)
        return self

    def fake(self) -> Self:
        """
        Indicates that the file should "fake" its creation when committing.
        """
        self.will_fake = True
        return self

    def restore(self) -> Self:
        """
        Indicates that the file should not "fake" when committing.
        """
        self.will_fake = False
        return self

    def generate(self) -> str:
        """
        Generate the file's content.

        Raises
        ------
        :py:exc:`fabricius.generator.errors.NoContentError` :
            If no content to the file were added.

        Returns
        -------
        :py:class:`str` :
            The final content of the file.
        """
        if not self.content:
            raise NoContentError(self.name)

        return self.renderer(self.data).render(self.content)

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
        :py:exc:`fabricius.generator.errors.NoContentError` :
            If no content to the file were added.
        :py:exc:`fabricius.generator.errors.NoDestinationError` :
            If no destination/path were designated.
        :py:exc:`fabricius.generator.errors.AlreadyCommittedError` :
            If the file has already been saved to the disk.
        :py:exc:`FileExistsError` :
            If the file already exists on the disk and ``overwrite`` is set to ``False``.

            This is different from
            :py:exc:`AlreadyCommittedError <fabricius.generator.errors.AlreadyCommittedError>`
            because this indicates that the content of the file this generator was never actually
            saved.
        :py:exc:`OSError` :
            The file's name is not valid for the OS.

        Returns
        -------
        :py:class:`fabricius.file.FileCommitResult` :
            A typed dict with information about the created file.
        """
        if not self.destination:
            raise NoDestinationError(self.name)
        if not self.content:
            raise NoContentError(self.name)
        if self.state == "persisted":
            raise AlreadyCommittedError(self.name)

        final_content = self.generate()

        if not self.destination.exists() and (not self.will_fake):
            self.destination.mkdir(parents=True)
        destination = self.destination.joinpath(self.name)

        if destination.exists() and not overwrite:
            raise FileExistsError(f"File '{self.name}' already exists.")

        if self.will_fake:
            self.state = "persisted"
        else:
            with contextlib.suppress(NotADirectoryError):
                destination.write_text(final_content)
                self.state = "persisted"

        return FileCommitResult(
            name=self.name,
            state=self.state,
            data=self.data,
            template_content=self.content,
            content=final_content,
            destination=self.destination.joinpath(self.name),
        )
