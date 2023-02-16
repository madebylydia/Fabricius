import typing
from typing_extensions import Self
from copy import copy

from .file import (
    AlreadyCommittedError,
    File,
    FileCommitResult,
    NoContentError,
    NoDestinationError,
)
from .plugin import AcceptPlugins
from .plugins.define import GeneratorPlugin


GPlugin = typing.cast(GeneratorPlugin, GeneratorPlugin)


class Generator(AcceptPlugins[GeneratorPlugin]):
    files: typing.List[File]
    """
    The list of files to generate with the generator.
    """

    results: typing.Dict[File, typing.Optional[FileCommitResult]] = {}
    """
    The result of each file commit.
    """

    _fake: bool
    """
    If the generator should create the files or not.
    """

    def __init__(self) -> None:
        self.files = []
        self._fake = False
        super().__init__()

    def connect_plugin(
        self, plugin: GeneratorPlugin, *, force_append: bool = False
    ) -> GeneratorPlugin:
        plugin = super().connect_plugin(plugin, force_append=force_append)
        plugin.generator = self
        return plugin

    def _execute_file(self, file: File, allow_overwrite: bool) -> FileCommitResult | None:
        """
        Attempt to commit a file and return its result.
        """
        if self._fake:
            file.fake()

        try:
            self.send_to_plugins(GPlugin.before_file_commit, file=file)
            try:
                file_result = file.commit(overwrite=allow_overwrite)
            except FileExistsError:
                file_result = None
            self.send_to_plugins(GPlugin.after_file_commit, file=file, result=file_result)

            return file_result

        except (
            NoContentError,
            NoDestinationError,
            FileExistsError,
            AlreadyCommittedError,
        ) as error:
            self.send_to_plugins(GPlugin.on_commit_fail, file=file, exception=error)
            return None
            # Was there a real reason to separate this error handling?

        except Exception as error:
            self.send_to_plugins(GPlugin.on_commit_fail, file=file, exception=error)
            return None

    def fake(self) -> Self:
        """
        Tell the generator to not generate files upon execution.
        Used for testing purposes.

        .. warning::
           Plugins you connect will not directly know that you've been faking file's
           generation, they will get the file's result as if it were correctly saved
           onto the disk. This might create unexpected exceptions.
        """
        self._fake = True
        return self

    def restore(self) -> Self:
        """
        Tell the generator to generate files upon execution.
        Used for testing purposes.
        """
        self._fake = False
        return self

    def add_file(self, name: str, extension: typing.Optional[str] = None) -> File:
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
        :py:class:`fabricius.file.File` :
            The generated file. You then have to set file's options.
        """
        file = File(name, extension)
        self.files.append(file)
        self.send_to_plugins(GPlugin.on_file_add, file=file)
        return file

    def execute(self, *, allow_overwrite: bool = False) -> typing.Dict[File, typing.Optional[FileCommitResult]]:
        """
        Execute generator's tasks.

        Parameters
        ----------
        allow_overwrite : :py:class:`bool`
            If files exist at their set path, shall this parameter say if files should be
            overwritten or not.

        Returns
        -------
        Dict[:py:class:`fabricius.file.File`, :py:class:`fabricius.file.FileCommitResult`] :
            A dict containing a file generator and its commit result.
            In case the value is ``None``, this mean that the file was not successfully saved to
            the disk (Already committed, file already exists, etc.).
        """
        self.send_to_plugins(GPlugin.before_execution)

        for file in self.files:
            if result := self._execute_file(file, allow_overwrite):
                self.results[file] = result

        results = copy(self.results)

        for file in self.files:
            if file not in results.keys():
                results[file] = None

        self.send_to_plugins(GPlugin.after_execution, results=results)
        return results
