import contextlib
import pathlib
import typing

from typing_extensions import Self

from fabricius.app.signals import after_file_commit, before_file_commit
from fabricius.exceptions import AlreadyCommittedError, MissingRequiredValueError
from fabricius.models.renderer import Renderer
from fabricius.renderers import (
    ChevronRenderer,
    JinjaRenderer,
    PythonFormatRenderer,
    StringTemplateRenderer,
)
from fabricius.types import FILE_STATE, Data, FileCommitResult, PathStrOrPath


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

    template_content: str | None
    """
    The content of the base template, if set.
    """

    destination: pathlib.Path | None
    """
    The destination of the file, if set.
    """

    renderer: type[Renderer]
    """
    The renderer to use to generate the file.
    """

    data: Data
    """
    The data that will be passed to the renderer.
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

        self.renderer = PythonFormatRenderer
        self.data = {}

    def compute_destination(self) -> pathlib.Path:
        """
        Compute the destination of the file.

        Returns
        -------
        pathlib.Path :
            The final path.
        """
        if not self.destination:
            raise MissingRequiredValueError(self, "destination")

        if not self.destination.exists() and (not self._will_fake):
            self.destination.mkdir(parents=True)
        return self.destination.joinpath(self.name)

    @property
    def can_commit(self) -> typing.Literal["destination", "content", "state", True]:
        # sourcery skip: reintroduce-else
        if not self.destination:
            return "destination"
        if not self.content:
            return "content"
        if self.state == "persisted":
            return "state"

        return True

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

    def use_jinja(self) -> Self:
        """
        Use Jinja2 to render the template.
        """
        self.renderer = JinjaRenderer
        return self

    def with_renderer(self, renderer: typing.Type[Renderer]) -> Self:
        """
        Use a custom renderer to render the template.

        Parameters
        ----------
        renderer : Type of :py:class:`fabricius.generator.renderer.Renderer`
            The renderer to use to format the file.
            It must be not initialized.
        """
        self.renderer = renderer
        return self

    def with_data(self, data: Data, *, overwrite: bool = True) -> Self:
        """
        Add data to pass to the template.

        Parameters
        ----------
        data : :py:data:`fabricius.const.Data`
            The data you want to pass to the template.
        overwrite : :py:class:`bool`
            If the data that already exists should be deleted. If False, the new data will be
            added on top of the already existing data. Default to ``True``.
        """
        if overwrite:
            self.data = {}
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
           This is the default behavior. It's only useful to use this method if you have used :py:meth:`.fake`.
        """
        self._will_fake = False
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
            raise MissingRequiredValueError(self, "content")

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
        :py:exc:`fabricius.exceptions.AlreadyCommittedError` :
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
            raise MissingRequiredValueError(self, "destination")
        if not self.content:
            raise MissingRequiredValueError(self, "content")
        if self.state == "persisted":
            raise AlreadyCommittedError(self.name)

        final_content = self.generate()

        destination = self.compute_destination()

        if destination.exists() and not overwrite:
            exception = FileExistsError(f"File '{self.name}' already exists.")
            exception.filename = self.name
            raise exception

        if self._will_fake:
            self.state = "persisted"
        else:
            with contextlib.suppress(NotADirectoryError):
                destination.write_text(final_content)
                self.state = "persisted"

        before_file_commit.send(self)

        commit = FileCommitResult(
            name=self.name,
            state=self.state,
            data=self.data,
            template_content=self.content,
            content=final_content,
            destination=self.destination.joinpath(self.name),
            fake=self._will_fake,
        )

        after_file_commit.send(self)
        return commit
