import pathlib
from abc import abstractmethod
from typing import Optional, Type, TypedDict

from typing_extensions import Self

from fabricius.const import FILE_STATE, Data

from .file_base import BaseFileContract
from .renderer import RendererContract


class CommitResult(TypedDict):
    """
    Return the result of a file commit.
    """

    state: FILE_STATE
    """
    The state of the file.
    """

    with_data: Data
    """
    The data that has been passed to the file when rendering.
    """

    with_renderer: Type[RendererContract]
    """
    The renderer that has rendered the template.
    """

    template_content: str
    """
    The content of the template.
    """

    content: str
    """
    The final content of the file once created.
    """

    path: pathlib.Path
    """
    The path of the file.
    """


class GeneratorFileExport(TypedDict):
    """
    A TypedDict object. Used for :py:func:`FileGeneratorContract.to_dict <FileGeneratorContract.to_dict>`.
    """

    name: str
    """
    The name of the file.
    """

    state: FILE_STATE
    """
    The actual state of the file.
    """

    template_content: Optional[str]
    """
    The content of the template file, if any.
    """

    destination: Optional[pathlib.Path]
    """
    The selected destination for the file, if any.
    """

    renderer: Type[RendererContract]
    """
    The renderer that will render the result.
    """

    data: Data
    """
    The data that will be passed the the renderer.
    """


class FileGeneratorContract(BaseFileContract):
    content: Optional[str]
    """
    The content of the template.
    """

    destination: Optional[pathlib.Path]
    """
    The selected destination.
    """

    renderer: Type[RendererContract]
    """
    The renderer used to render the template.
    """

    data: Data
    """
    The data that will be passed to the renderer.
    """

    @abstractmethod
    def __init__(self, name: str, extension: Optional[str]) -> None:
        """
        Create a file's generator.

        Parameters
        ----------
        name : :py:class:`str`
            The name of the file.
        extension : Optional, :py:class:`str`
            The extension of the file, without dot, same as ``name="<name>.<extension>"``
        """
        raise NotImplementedError()

    @abstractmethod
    def from_file(self, path: str | pathlib.Path) -> Self:
        """
        Read the content from a file template.

        Parameters
        ----------
        path : :py:class:`str` or :py:class:`pathlib.Path`
            The path of the file template.
        """
        raise NotImplementedError()

    @abstractmethod
    def from_content(self, content: str) -> Self:
        """
        Read the content from a string.

        Parameters
        ----------
        content : :py:class:`str`
            The template you want to format.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_directory(self, directory: str | pathlib.Path, *, recursive: bool = True) -> Self:
        """
        Set the directory where the file will be saved.

        Raises
        ------
        :py:exc:`FileNotFoundError` :
            The given directory does not exist. (And recursive is set to False)

        Parameters
        ----------
        directory : :py:class:`str` or :py:class:`pathlib.Path`
            Where the file will be stored. Does not include the file's name.
        recursive : :py:class:`bool`
            Create the parents folder if not existing. Default to True.
        """
        raise NotImplementedError()

    @abstractmethod
    def use_mustache(self) -> Self:
        """
        Use chevron (Mustache) to render the template.
        """
        raise NotImplementedError()

    @abstractmethod
    def use_string_template(self) -> Self:
        """
        Use string.Template to render the template.
        """
        raise NotImplementedError()

    @abstractmethod
    def with_renderer(self, renderer: Type[RendererContract]) -> Self:
        """
        Use a custom renderer to render the template.

        Parameters
        ----------
        renderer : Type[:py:class:`.RendererContract`]
            A renderer that implements :py:class:`.RendererContract`.
            It must be not initialized.
        """

    @abstractmethod
    def with_data(self, data: Data, *, overwrite: bool = False) -> Self:
        """
        Add data to pass to the template.

        Parameters
        ----------
        data : :py:data:`.Data`
            The data you want to pass to the template.
        overwrite : :py:class:`bool`
            If the data that already exists should be deleted. If False, the new data will be
            added on top of the already existing data.
        """
        raise NotImplementedError()

    @abstractmethod
    def generate(self) -> str:
        """
        Generate the file's content.

        Raises
        ------
        :py:exc:`NoContentError` :
            If no content to the file were added.

        Returns
        -------
        :py:class:`str` :
            The final content of the file.
        """
        raise NotImplementedError()

    @abstractmethod
    def commit(self, *, overwrite: bool = False) -> CommitResult:
        """
        Save the file using this class.

        Parameters
        ----------
        overwrite : :py:class:`bool`
            If a file exist at the given path, shall the overwrite parameter say if the file should be overwritten or net.

        Raises
        ------
        :py:exc:`NoContentError` :
            If no content to the file were added.
        :py:exc:`NoDestinationError` :
            If no destination/path were designated.

        Returns
        -------
        :py:class:`CommitResult` :
            A dict with information about the created file.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> GeneratorFileExport:
        """
        Export the class to a typed dict.

        Returns
        -------
        :py:class:`GeneratorFileExport` :
            The exported dict.
        """
        raise NotImplementedError()
