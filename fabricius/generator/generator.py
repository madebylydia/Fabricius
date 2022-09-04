from typing import Dict, List, Optional, ParamSpec, cast

from fabricius.generator.errors import (
    AlreadyCommittedError,
    NoContentError,
    NoDestinationError,
)
from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.interfaces import SupportsPlugin
from fabricius.plugins.generator import GeneratorPlugin

_P = ParamSpec("_P")

Plugin = cast(GeneratorPlugin, GeneratorPlugin)
# That might seems useless, but this is to trick static type checkers when using "_plugin_call"
# If we use "GeneratorPlugin" directly with "_plugin_call", we will also get the "self" args in
# the way, by using this variable, we get rid of the "self" and everyone's happy!


class Generator(SupportsPlugin):
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
        self._plugin_call(Plugin.on_file_add, file=file)
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
            the disk (Already commited, file already exists, etc.).
        """
        result: Dict[FileGenerator, Optional[GeneratorCommitResult]] = {}

        self._plugin_call(Plugin.before_execution)

        for file in self.files:

            try:
                self._plugin_call(Plugin.before_file_commit, file=file)
                file_result = file.commit(overwrite=allow_overwrite, dry_run=dry_run)
                self._plugin_call(Plugin.after_file_commit, file=file)

                result[file] = file_result

            except (
                NoContentError,
                NoDestinationError,
                FileExistsError,
                AlreadyCommittedError,
            ) as error:
                self._plugin_call(Plugin.on_commit_fail, file=file, exception=error)

            except Exception as error:
                self._plugin_call(Plugin.on_commit_fail, file=file, exception=error)

        self._plugin_call(Plugin.after_execution, results=result)
        return result
