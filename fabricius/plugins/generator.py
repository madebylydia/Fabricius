from typing import TYPE_CHECKING, Any, Dict, Optional

from fabricius.file import File, FileCommitResult
from fabricius.interfaces import BasePlugin

if TYPE_CHECKING:
    from fabricius.generator import Generator


class GeneratorPlugin(BasePlugin):
    """
    A plugin to plug to the :py:class:`fabricius.generator.generator.Generator` class.

    You can edit the methods of the class, and they'll be run according to their description.
    """

    generator: "Generator"
    """
    The generator that the plugin is connected to.
    """

    def on_file_add(self, file: File) -> Any:
        """
        Called when a new file has been added to the generator.

        Parameters
        ----------
        file : :py:class:`fabricius.file.File`
            The file that has been added to the generator.
        """
        raise NotImplementedError()

    def before_execution(self) -> Any:
        """
        Called when the user has called the "execute" method.
        This is ran before the generator creates any files.
        """
        raise NotImplementedError()

    def before_file_commit(self, file: File) -> Any:
        """
        Called when a file is about to be created.
        The file is NOT yet created and is still not saved locally.

        Parameters
        ----------
        file : :py:class:`fabricius.file.File`
            The file that will be generated.
        """
        raise NotImplementedError()

    def after_file_commit(self, file: File, result: Optional[FileCommitResult]) -> Any:
        """
        Called when a file has been created and saved locally.

        Parameters
        ----------
        file : :py:class:`fabricius.file.File`
            The file that has been generated.
        """
        raise NotImplementedError()

    def after_execution(self, results: Dict[File, Optional[FileCommitResult]]) -> Any:
        """
        Called when the generator has realized all file generation.

        Parameters
        ----------
        results : List of :py:class:`fabricius.file.GeneratorFileCommitResult`
            A list of
            :py:class:`GeneratorFileCommitResult <fabricius.file.GeneratorFileCommitResult>`.
        """
        raise NotImplementedError()

    def on_commit_fail(self, file: File, exception: Exception) -> Any:
        """
        Called when the generator has failed to commit a file.

        Parameters
        ----------
        file : :py:class:`fabricius.file.File`
            The file that has been generated.
        exception : :py:class:`Exception`
            The exception that was raised.
        """
        raise NotImplementedError()
