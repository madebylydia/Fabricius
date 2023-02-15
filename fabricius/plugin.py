import re
import typing

from fabricius.errors import PluginConnectionError


PIID_REGEX = re.compile(r"^([a-z]{3,})-(\d{6})$")


class Plugin(typing.Protocol):
    """
    The base class for all plugins.
    """

    PIID: typing.ClassVar[typing.Optional[str]] = None
    """
    The PIID (Plugin Identifier & ID) is a string composed of a name for the plugin that is created
    """

    _is_connected: bool

    def __init__(self) -> None:
        self._is_connected = False

    @property
    def has_valid_piid(self) -> bool:
        """
        Return a boolean indicating if the plugin has a PIID assigned.
        This will return False if no PIID are assigned.

        Returns
        -------
        `:py:class:`bool` :
            If the plugin has a valid PIID.
        """
        if not self.PIID:
            return False
        piid = PIID_REGEX.match(self.PIID)
        return piid is not None

    @property
    def plugin_name(self) -> typing.Optional[str]:
        """Return the name of the plugin based on the PIID.

        Returns
        -------
        Optional, :py:class:`str` :
            The name of the plugin if defined and valid.
        """
        return PIID_REGEX.match(self.PIID).group(1) if self.has_valid_piid else None  # type: ignore

    @property
    def plugin_id(self) -> typing.Optional[int]:
        """Return the ID of the plugin base on the PIID.

        Returns
        -------
        Optional, :py:class:`int` :
            The ID of the plugin if defined and valid.
        """
        return int(PIID_REGEX.match(self.PIID).group(2)) if self.has_valid_piid else None  # type: ignore

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def setup(self) -> typing.Any:
        """
        Called when the plugin has been connected to the class.
        """
        raise NotImplementedError()

    def teardown(self) -> typing.Any:
        """
        Called when a plugin is about to be disconnected of the class.
        """
        raise NotImplementedError()


_P = typing.ParamSpec("_P")
"""
ParamSpec to help with AcceptPlugins.send_to_plugins to retransmit the types and return type.
"""
_PT = typing.TypeVar("_PT", bound=Plugin)
"""
TypeVar indicating which plugin class (Subclass of Plugin) can be accepted.
"""


class AcceptPlugins(typing.Generic[_PT]):
    """
    Define a class that can support plugin addition.
    To use this class, you must subclass it in your own class that will accept plugins, and by
    specifying which plugin subclass are accepted. For example:

    .. code-block:: python

       from fabricius.plugin import Plugin, AcceptPlugins

       class GeneratorPlugin(Plugin):
           # Create your plugin here

       class Generator(AcceptPlugins[GeneratorPlugin]):
           # Create your class here, only subclass of GeneratorPlugin are accepted in this class.

    Plugins works using events, they receive events, like "on_generator_execute", which, for
    example, is called when the generator is going to be executed. As such, the class that emits
    is the emitter (Back to our example, it is Generator), and the plugin is the receiver.
    To emit an event in the emitter class, you can call the
    :py:meth:`send_to_plugins` method.

    .. code-block:: python

       class Generator(AcceptPlugins[GeneratorPlugin]):
           ...

           def execute(self):
               files = self.get_files()

               # Send the "on_generator_execute" event, with files as a parameter.
               self.send_to_plugins(GeneratorPlugin.on_generator_execute, files=files)
    """

    _plugins: typing.List[_PT]
    """
    A list of plugins connect within the class.
    """

    def __init__(self) -> None:
        self._plugins = []

    def _search_connected_plugin(self, plugin: typing.Type[_PT]) -> typing.Optional[_PT]:
        """
        Look up connected plugins and return a plugin if a same instance of the given plugin is
        found.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.plugin.Plugin`
            The plugin to look for.

        Returns
        -------
        Optional, instance of :py:class:`fabricius.plugin.Plugin` :
            The connected plugin, if any.
        """
        for connected_plugin in self._plugins:
            if isinstance(connected_plugin, plugin):
                return connected_plugin

    def connect_plugin(self, plugin: _PT, *, force_append: bool = False) -> _PT:
        """
        Add (Connect) a plugin to the class.

        Parameters
        ----------
        plugin : :py:class:`fabricius.plugin.Plugin`
            The plugin to connect.
        force_append : :py:class:`bool`
            In case the plugin's setup did not succeed (Thrown an exception), it will not be
            added to the class's plugins. Setting this value to ``True`` will always append
            the plugin to the class's plugins even when it fails to set up.
            This will also avoid raising
            :py:exc:`PluginConnectionError <fabricius.errors.PluginConnectionError>` when failing.

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

        if self._search_connected_plugin(plugin.__class__):
            raise PluginConnectionError(
                plugin.__class__.__name__, "Plugin is already connected to the generator."
            )

        try:
            plugin.setup()
        except NotImplementedError:
            pass
        except Exception as error:
            if not force_append:
                raise PluginConnectionError(
                    plugin.plugin_name or plugin.__class__.__name__,
                    f"Plugin's setup has thrown an exception: {error}"
                ) from error

        self._plugins.append(plugin)
        plugin._is_connected = True  # type: ignore
        return plugin

    def disconnect_plugin(self, plugin: _PT | typing.Type[_PT]) -> None:
        """
        Remove (Disconnect) a plugin to this generator.

        In case the plugin throws an error while tearing down, the plugin will still be removed
        from the generator's plugins.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.plugin.Plugin` or :py:class:`fabricius.plugin.Plugin`
            The plugin to disconnect.
        """
        # Obtain the non-initialized class of plugin
        plugin_class = plugin if isinstance(plugin, type) else plugin.__class__

        if connected_plugin := self._search_connected_plugin(plugin_class):
            try:
                connected_plugin.teardown()
            finally:
                self._plugins.remove(connected_plugin)
                connected_plugin._is_connected = False  # type: ignore


    def send_to_plugins(
        self,
        method: typing.Callable[_P, None],
        silence_exceptions: bool = False,
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        """
        Call a given method for all connected plugins.
        If a plugin did not implement the method, it'll get skipped.

        Parameters
        ----------
        method : Callable[_P, None]
            The method to call.
        silence_exceptions : bool
            If a plugin throws an exception, this parameter will tell if it should ignore it or
            raise it. Defaults to False.
        *args : _P.args
            The arguments to pass.
        **kwargs : _P.kwargs
            The positional arguments to pass.

        Raises
        ------
        :py:exc:`Exception` :
            Any exception raised by a plugin, only raisable if ``silence_exceptions`` is set to
            ``False``.
        """
        to_call = typing.cast(
            typing.List[typing.Optional[typing.Callable[_P, None]]],
            [getattr(plugin, method.__name__, None) for plugin in self._plugins ],
        )
        to_call = [method for method in to_call if method]

        for func in to_call:
            try:
                func(*args, **kwargs)
            except Exception as exception:
                if silence_exceptions:
                    continue

                raise exception
