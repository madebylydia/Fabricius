from abc import ABC, abstractmethod
from typing import List, Optional

from fabricius.contracts.file_generator import CommitResult

from .file_generator import GeneratorFileContract


class GeneratorContract(ABC):
    files: List[GeneratorFileContract]

    @abstractmethod
    def add_file(self, name: str, extension: Optional[str] = None) -> GeneratorFileContract:
        """
        Add a file to the generator.

        Parameters
        ----------
        name : str
            The name of the file
        extension: Optional, str
            The extension of the file, can be optional.
            If none, no extension will be added.

        Returns
        -------
        GeneratorFileContract :
            The generated file. You then have to set file's options.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self) -> List[CommitResult]:
        """
        Execute generator's tasks.

        Returns
        -------
        """
        raise NotImplementedError()
