from typing import Any, Callable, List, Optional, Type, ParamSpec, cast

from fabricius.errors import PluginConnectionError


class BasePlugin:
    def setup(self) -> Any:
        """
        Called when the plugin has been connected to the class.
        """
        raise NotImplementedError()

    def teardown(self) -> Any:
        """
        Called when a plugin is about to be disconnected of the class.
        """
        raise NotImplementedError()


_P = ParamSpec("_P")


class SupportsPlugin():
    plugins: List[BasePlugin]
    """
    A list of plugins to use with the class.
    """

    def __init__(self) -> None:
        self.plugins = []

    def __search_connected_plugin(
        self, plugin: Type[BasePlugin]
    ) -> Optional[BasePlugin]:
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

    def connect_plugin(self, plugin: BasePlugin, *, force_append: bool = False):
        """
        Add (Connect) a plugin to the class.

        Parameters
        ----------
        plugin : py:class:`fabricius.plugins.generator.GeneratorPlugin`
            The plugin to connect.
        force_append : :py:class:`bool`
            In case the plugin's setup did not succeed (Thrown an exception), it will not be
            added to the class's plugins. Setting this value to ``True`` will always append
            the plugin to the class's plugins even when it fails to setup.
            This will also avoid raising ``PluginConnectionError`` when failing.

        Raises
        ------
        :py:exc:`fabricius.errors.PluginConnectionError` :
            If the plugin is already connected to the class, this error is raised.
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

    def disconnect_plugin(self, plugin: Type[BasePlugin] | BasePlugin) -> bool:
        """
        Remove (Disconnect) a plugin to this generator.

        In case the plugin throws an error while tearing down, the plugin will still be removed
        from the generator's plugins.

        Parameters
        ----------
        plugin : :py:class:`fabricius.plugins.generator.GeneratorPlugin`
            The plugin to disconnect.

        Returns
        -------
        :py:class:`bool` :
            True if the plugin was successfully removed.
        """
        plugin_class = plugin if isinstance(plugin, type) else plugin.__class__
        if connected_plugin := self.__search_connected_plugin(plugin_class):
            try:
                connected_plugin.teardown()
            finally:
                self.plugins.remove(connected_plugin)
        return True

    def _plugin_call(
        self, method: Callable[_P, None], *args: _P.args, **kwargs: _P.kwargs
    ) -> bool:
        """Call the given method for all connected plugins.

        Parameters
        ----------
        method : Callable[..., None]
            The method to call.

        """
        function_name = method.__name__
        for plugin in self.plugins:
            function = cast(Callable[_P, None], getattr(plugin, function_name))
            try:
                function(*args, **kwargs)
            except NotImplementedError:
                return False
        return True
