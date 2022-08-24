import os
from typing import Callable, Dict, List, Optional, ParamSpec, Type, cast

from fabricius.generator.errors import (
    AlreadyCommittedError,
    NoContentError,
    NoDestinationError,
    PluginConnectionError,
)
from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.generator.reporter import Reporter
from fabricius.plugins.generator import GeneratorPlugin

_P = ParamSpec("_P")

Plugin: GeneratorPlugin = GeneratorPlugin  # type: ignore
# That might seems useless, but this is to trick static type checkers when using "_plugin_call"
# If we use "GeneratorPlugin" directly with "_plugin_call", we will also get the "self" args in
# the way, by using this variable, we get rid of the "self" and everyone's happy!


class Generator:
    reporter: Reporter
    """
    The reporter.
    """

    files: List[FileGenerator]
    """
    The list of files to generate with the generator.
    """

    plugins: List[GeneratorPlugin]
    """
    A list of plugins to use with the generator.
    """

    def __init__(self) -> None:
        self.reporter = Reporter()
        self.files = []
        self.plugins = []

    def __search_connected_plugin(
        self, plugin: Type[GeneratorPlugin]
    ) -> Optional[GeneratorPlugin]:
        """
        Look up connected plugins and return a plugin if a same instance of the given plugin is
        found.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.plugins.generator.GeneratorPlugin`
            The plugin to look for.

        Returns
        -------
        Optional, :py:class:`fabricius.plugins.generator.GeneratorPlugin` :
            The connected plugin, if any.
        """
        for connected_plugin in self.plugins:
            if isinstance(connected_plugin, plugin):
                return connected_plugin

    def connect_plugin(self, plugin: GeneratorPlugin, *, force_append: bool = False):
        """
        Add (Connect) a plugin to this generator.

        Parameters
        ----------
        plugin : py:class:`fabricius.plugins.generator.GeneratorPlugin`
            The plugin to connect.
        force_append : :py:class:`bool`
            In case the plugin's setup did not succeed (Thrown an exception), it will not be
            added to the generator's plugins. Setting this value to ``True`` will always append
            the plugin to the generator's plugins even when it fails to setup.
            This will also avoid raising ``PluginConnectionError`` when failing.

        Raises
        ------
        :py:exc:`fabricius.generator.errors.PluginConnectionError` :
            If the plugin is already connected to the generator, this error is raised.
            This error is also raised when the plugin's setup process has thrown an exception.

        Returns
        -------
        :py:class:`bool` :
            If the plugin was successfully added.
        """
        if self.__search_connected_plugin(plugin.__class__):
            raise PluginConnectionError(
                plugin.__class__.__name__, "Plugin is already connected to the generator."
            )

        try:
            plugin.setup()
        except Exception as error:
            if not force_append:
                raise PluginConnectionError(
                    plugin.__class__.__name__, f"Plugin's setup has thrown an exception: {error}"
                ) from error

        self.plugins.append(plugin)
        return True

    def disconnect_plugin(self, plugin: Type[GeneratorPlugin] | GeneratorPlugin) -> bool:
        """
        Remove (Disconnect) a plugin to this generator.

        In case the plugin throws an error while tearing down, the plugin will still be removed
        from the generator's plugins.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.plugins.generator.GeneratorPlugin`
            The plugin to disconnect.

        Returns
        -------
        :py:class:`bool` :
            True if the plugin was successfully removed. False
        """
        if connected_plugin := self.__search_connected_plugin(
            plugin.__class__ if isinstance(plugin, GeneratorPlugin) else plugin
        ):
            try:
                connected_plugin.teardown()
            finally:
                self.plugins.remove(connected_plugin)
                return True
        return False

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
                file_result = file.commit(overwrite=allow_overwrite, dry_run=True)
                self._plugin_call(Plugin.after_file_commit, file=file)

                cwd_path = file_result["destination"].relative_to(os.getcwd())

                self.reporter.success(f"{cwd_path} ({file.name})")
                result[file] = file_result

            except (
                NoContentError,
                NoDestinationError,
                FileExistsError,
                AlreadyCommittedError,
            ) as error:
                self._plugin_call(Plugin.on_commit_fail, file=file, exception=error)
                self.reporter.skip(f"{file.name} - {error}")

            except Exception as error:
                self._plugin_call(Plugin.on_commit_fail, file=file, exception=error)
                self.reporter.fail(file.name)
                self.reporter.console.print_exception(extra_lines=0)

        self._plugin_call(Plugin.after_execution, results=result)

        return result

    def _plugin_call(
        self, method: Callable[_P, None], *args: _P.args, **kwargs: _P.kwargs
    ) -> bool:
        """
        Call a method for all plugins.
        """
        function_name = method.__name__
        for plugin in self.plugins:
            function = cast(Callable[_P, None], getattr(plugin, function_name))
            try:
                function(*args, **kwargs)
            except NotImplementedError:
                return False
        return True
