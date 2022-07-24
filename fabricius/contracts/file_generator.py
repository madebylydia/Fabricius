import pathlib
from abc import abstractmethod
from typing import Optional, Type, TypedDict

from typing_extensions import Self

from fabricius.const import FILE_STATE, Data

from .file_base import BaseFile
from .renderer import RendererContract


class CommitResult(TypedDict):
    """
    Return the result of a file commit.

    .. property:: state

       The state of the file.

       :type: :py:const:`FILE_STATE <fabricius.const.FILE_STATE>`

    .. property:: with_data

       The data that has been passed to the file when rendering.
       None if the commit failed.

       :type: Optional, :py:const:`Data <fabricius.const.Data>`

    .. property:: content

       The final content of the file once created.

       :type: :py:class:`str`

    .. property:: path

       The path of the file.
       None if the commit failed.

       :type: Optional, :py:class:`pathlib.Path`

    """

    state: FILE_STATE
    with_data: Data
    template_content: str
    content: str
    path: pathlib.Path


class GeneratorFileExport(TypedDict):
    """
    A TypedDict object. Used for :py:func:`GeneratorFileContract.to_dict`.

    .. property:: name

       The name of the file.

       :type: :py:class:`str`

    .. property:: state

       The actual state of the file.

       :type: :py:data:`.FILE_STATE`

    .. property:: template_content

       The content of the template file, if any.

       :type: Optional, :py:class:`str`

    .. property:: destination

       The selected destination for the file, if any.

       :type: Optional, :py:class:`pathlib.Path`

    .. property:: renderer

       The renderer that will render the result.

       :type: Type[:py:class:`.RendererContract`]
    """

    name: str
    state: FILE_STATE

    template_content: Optional[str]
    destination: Optional[pathlib.Path]

    renderer: Type[RendererContract]
    data: Data


class GeneratorFileContract(BaseFile):
    content: Optional[str]
    destination: Optional[pathlib.Path]

    renderer: Type[RendererContract]
    data: Data

    @abstractmethod
    def __init__(self, name: str, extension: Optional[str]) -> None:
        """
        Create a file's generator.

        Parameters
        ----------
        name : str
            The name of the file.
        extension : str
            The extension of the file, without dot, same as ``name="<name>.<extension>"``
        """
        raise NotImplementedError()

    @abstractmethod
    def from_file(self, path: str | pathlib.Path) -> Self:
        """
        Read the content from a file template.

        Parameters
        ----------
        path : str or pathlib.Path
            The path of the file template.
        """
        raise NotImplementedError()

    @abstractmethod
    def from_content(self, content: str) -> Self:
        """
        Read the content from a string.

        Parameters
        ----------
        content : str
            The template you want to format.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_directory(self, directory: str | pathlib.Path, *, recursive: bool = False) -> Self:
        """
        Set the directory where the file will be saved.

        Raises
        ------
        FileNotFoundError :
            The given directory does not exist. (And recursive is set to False)

        Parameters
        ----------
        directory : str or pathlib.Path
            Where the file will be stored. Does not include the file's name.
        recursive : bool
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
        renderer : Type[RendererContract]
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
        overwrite : bool
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
        NoContentError :
            If no content to the file were added.

        Returns
        -------
        str :
            The final content of the file.
        """
        raise NotImplementedError()

    @abstractmethod
    def commit(self, *, overwrite: bool = False) -> CommitResult:
        """
        Save the file using this class.

        Parameters
        ----------
        overwrite : bool
            If a file exist at the given path, shall the overwrite parameter say if the file should be overwritten or net.

        Raises
        ------
        NoContentError :
            If no content to the file were added.
        NoDestinationError :
            If no destination/path were designated.

        Returns
        -------
        CommitResult :
            A dict with information about the created file.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> GeneratorFileExport:
        """
        Export the class to a typed dict.

        Returns
        -------
        GeneratorFileExport :
            The exported dict.
        """
        raise NotImplementedError()
