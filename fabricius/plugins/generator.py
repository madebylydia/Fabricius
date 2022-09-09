from typing import Any, Dict, Optional

from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.interfaces import BasePlugin


class GeneratorPlugin(BasePlugin):
    """
    A plugin to plug to the :py:class:`fabricius.generator.generator.Generator` class.

    You can edit the methods of the class and they'll be run according to their description.
    """

    def on_file_add(self, file: FileGenerator) -> Any:
        """
        Called when a new file has been added to the generator.

        Parameters
        ----------
        file : :py:class:`fabricius.generator.file.FileGenerator`
            The file that has been added to the generator.
        """
        raise NotImplementedError()

    def before_execution(self) -> Any:
        """
        Called when the user has called the "execute" method.
        This is ran before the generator creates any files.
        """
        raise NotImplementedError()

    def before_file_commit(self, file: FileGenerator) -> Any:
        """
        Called when a file is about to be created.
        The file is NOT yet created and is still not saved locally.

        Parameters
        ----------
        file : :py:class:`fabricius.generator.file.FileGenerator`
            The file that will be generated.
        """
        raise NotImplementedError()

    def after_file_commit(self, file: FileGenerator) -> Any:
        """
        Called when a file has been created and saved locally.

        Parameters
        ----------
        file : :py:class:`fabricius.generator.file.FileGenerator`
            The file that has been generated.
        """
        raise NotImplementedError()

    def after_execution(
        self, results: Dict[FileGenerator, Optional[GeneratorCommitResult]]
    ) -> Any:
        """
        Called when the generator has realized all file generation.

        Parameters
        ----------
        results : List of :py:class:`fabricius.generator.file.GeneratorCommitResult`
            A list of
            :py:class:`GeneratorCommitResult <fabricius.generator.file.GeneratorCommitResult>`.
        """
        raise NotImplementedError()

    def on_commit_fail(self, file: FileGenerator, exception: Exception) -> Any:
        """
        Called when the generator has failed to commit a file.

        Parameters
        ----------
        file : :py:class:`fabricius.generator.file.FileGenerator`
            The file that has been generated.
        exception : :py:class:`Exception`
            The exception that was raised.
        """
        raise NotImplementedError()
