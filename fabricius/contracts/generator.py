from abc import ABC, abstractmethod
from typing import List, Optional

from fabricius.contracts.file_generator import CommitResult

from .file_generator import FileGeneratorContract


class GeneratorContract(ABC):
    files: List[FileGeneratorContract]
    """
    The list of files to generate.

    .. warning:: Do not edit this property this yourself!
    """

    @abstractmethod
    def add_file(self, name: str, extension: Optional[str] = None) -> FileGeneratorContract:
        """
        Add a file to the generator.

        Parameters
        ----------
        name : :py:class:`str`
            The name of the file
        extension: Optional, :py:class:`str`
            The extension of the file, can be optional.
            If none, no extension will be added.

        Returns
        -------
        :py:class:`.FileGeneratorContract` :
            The generated file. You then have to set file's options.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self) -> List[CommitResult]:
        """
        Execute generator's tasks.

        Returns
        -------
        List of :py:class:`.CommitResult` :
            A list containing the result of each file's commit.
        """
        raise NotImplementedError()
