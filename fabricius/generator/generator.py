from typing import Dict, List, Optional, cast

from fabricius.generator.errors import (
    AlreadyCommittedError,
    NoContentError,
    NoDestinationError,
)
from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.interfaces import SupportsPlugin
from fabricius.plugins.generator import GeneratorPlugin

PluginType = cast(GeneratorPlugin, GeneratorPlugin)
# That might seem useless, but this is to trick static type checkers when using "_plugin_call"
# If we use "GeneratorPlugin" directly with "send_to_plugins", we will also get the "self" args in
# the way, by using this variable, we get rid of the "self" and everyone's happy!


class Generator(SupportsPlugin[GeneratorPlugin]):
    files: List[FileGenerator]
    """
    The list of files to generate with the generator.
    """

    def __init__(self) -> None:
        self.files = []
        super().__init__()

    def add_file(self, name: str, extension: Optional[str] = None) -> FileGenerator:
        """
        Add a file to the generator.

        Parameters
        ----------
        name : :py:class:`str`
            The name of the file
        extension : Optional, :py:class:`str`
            The extension of the file, can be optional.
            If none, no extension will be added.

        Returns
        -------
        :py:class:`fabricius.generator.file.FileGenerator` :
            The generated file. You then have to set file's options.
        """
        file = FileGenerator(name, extension)
        self.files.append(file)
        self.send_to_plugins(PluginType.on_file_add, file=file)
        return file

    def execute(
        self, *, allow_overwrite: bool = False, dry_run: bool = False
    ) -> Dict[FileGenerator, Optional[GeneratorCommitResult]]:
        """
        Execute generator's tasks.

        Parameters
        ----------
        allow_overwrite : :py:class:`bool`
            If files exist at their set path, shall this parameter say if files should be
            overwritten or not.
        dry_run : :py:class:`bool`
            You should not use this. This is mostly used for Fabricius's tests.
            This parameter indicate if files should be created.

        Returns
        -------
        Dict[:py:class:`fabricius.generator.file.FileGenerator`, :py:class:`fabricius.generator.file.CommitResult`] :
            A dict containing a file generator and its commit result.
            In case the value is ``None``, this mean that the file was not successfully saved to
            the disk (Already committed, file already exists, etc.).
        """
        result: Dict[FileGenerator, Optional[GeneratorCommitResult]] = {}

        self.send_to_plugins(PluginType.before_execution)

        for file in self.files:
            try:
                self.send_to_plugins(PluginType.before_file_commit, file=file)
                file_result = file.commit(overwrite=allow_overwrite, dry_run=dry_run)
                self.send_to_plugins(PluginType.after_file_commit, file=file)

                result[file] = file_result

            except (
                NoContentError,
                NoDestinationError,
                FileExistsError,
                AlreadyCommittedError,
            ) as error:
                self.send_to_plugins(PluginType.on_commit_fail, file=file, exception=error)
                # Was there a real reason to separate this error handling?

            except Exception as error:
                self.send_to_plugins(PluginType.on_commit_fail, file=file, exception=error)

        self.send_to_plugins(PluginType.after_execution, results=result)
        return result
