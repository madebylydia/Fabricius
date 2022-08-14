import pathlib
from abc import ABC, abstractmethod
from typing import Literal, Type, TypeAlias, TypedDict, Union

from typing_extensions import Self

TemplateType: TypeAlias = Literal["internal", "external"]


class TemplateDict(TypedDict):
    name: str
    """
    The name of the template.
    """

    path: pathlib.Path
    """
    Where the template is located.
    """

    type: TemplateType
    """
    The type of template.
    """


class TemplateContract(ABC):
    name: str
    """
    The name of the template.
    """

    path: pathlib.Path
    """
    Where the template is located.
    """

    type: TemplateType
    """
    The type of template.
    """

    @abstractmethod
    def to_dict(self) -> TemplateDict:
        """
        Export the object to a typed dict.

        Returns
        -------
        :py:class:`dict` :
            A typed dict of this class.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_cwd(cls: Type[Self], template_name_or_path: Union[str, pathlib.Path]) -> Self:
        """
        Obtain a template class from the current working directory.

        Parameters
        ----------
        template_name_or_path : :py:class:`str` or :py:class:`pathlib.Path`
            The name of the template or its path.

        Returns
        -------
        :py:class:`fabricius.Template` :
            This class.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_external_template(cls: Type[Self], alias: str) -> Self:
        """
        Obtain a template class from externals templates.

        Parameters
        ----------
        alias : :py:class:`str`
            The template's alias.

        Returns
        -------
        :py:class:`fabricius.Template` :
            This class.
        """
        raise NotImplementedError()
