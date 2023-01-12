import re
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Optional,
    ParamSpec,
    Protocol,
    Type,
    TypeVar,
    cast,
)

from typing_extensions import Self

from fabricius.errors import PluginConnectionError

PIID_REGEX = re.compile(r"^([a-z]{3,})-(\d{6})$")


class BasePlugin(Protocol):
    """
    The base class for all plugins.
    """

    PIID: Optional[str] = None
    """
    The PIID (Plugin Identifier & ID) is a string composed of a name for the plugin that is created
    """

    @property
    def has_valid_piid(self) -> bool:
        """
        Return a boolean indicating if the plugin has a PIID assigned.
        This will return False if no PIID are assigned.

        Returns
        -------
        bool :
            If the plugin has a valid PIID.
        """
        if not self.PIID:
            return False
        piid = PIID_REGEX.match(self.PIID)
        return piid is not None

    @property
    def plugin_name(self) -> Optional[str]:
        """Return the name of the plugin based on the PIID.

        Returns
        -------
        Optional[str] :
            The name of the plugin if defined and valid.
        """
        return PIID_REGEX.match(self.PIID).group(1) if self.has_valid_piid else None  # type: ignore

    @property
    def plugin_id(self) -> Optional[int]:
        """Return the ID of the plugin base on the PIID.

        Returns
        -------
        Optional[int] :
            The ID of the plugin if defined and valid.
        """
        return int(PIID_REGEX.match(self.PIID).group(2)) if self.has_valid_piid else None  # type: ignore

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
"""
A ParamSpec to help wit fabricius.interface.SupportsPlugin.send_to_plugins to
retransmit the types and return type.
"""
_PT = TypeVar("_PT", bound=BasePlugin)
"""
TypeVar indicating which plugin class (Subclass of fabricius.interface.BasePlugin)
can be accepted.
"""


class SupportsPlugin(Generic[_PT]):
    """
    Define a class that can support plugin addition.
    """

    plugins: List[_PT]
    """
    A list of plugins to use with the class.
    """

    def __init__(self) -> None:
        self.plugins = []

    def _search_connected_plugin(self, plugin: Type[_PT]) -> Optional[_PT]:
        """
        Look up connected plugins and return a plugin if a same instance of the given plugin is
        found.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.interfaces.BasePlugin`
            The plugin to look for.

        Returns
        -------
        Optional, instance of :py:class:`fabricius.interfaces.BasePlugin` :
            The connected plugin, if any.
        """
        for connected_plugin in self.plugins:
            if isinstance(connected_plugin, plugin):
                return connected_plugin

    def connect_plugin(self, plugin: _PT, *, force_append: bool = False) -> _PT:
        """
        Add (Connect) a plugin to the class.

        Parameters
        ----------
        plugin : :py:class:`fabricius.interfaces.BasePlugin`
            The plugin to connect.
        force_append : :py:class:`bool`
            In case the plugin's setup did not succeed (Thrown an exception), it will not be
            added to the class's plugins. Setting this value to ``True`` will always append
            the plugin to the class's plugins even when it fails to set up.
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
                    plugin.__class__.__name__, f"Plugin's setup has thrown an exception: {error}"
                ) from error

        self.plugins.append(plugin)
        return plugin

    def disconnect_plugin(self, plugin: _PT | Type[_PT]) -> bool:
        """
        Remove (Disconnect) a plugin to this generator.

        In case the plugin throws an error while tearing down, the plugin will still be removed
        from the generator's plugins.

        Parameters
        ----------
        plugin : Type of :py:class:`fabricius.interfaces.BasePlugin` or :py:class:`fabricius.interfaces.BasePlugin`
            The plugin to disconnect.

        Returns
        -------
        :py:class:`bool` :
            True if the plugin was successfully removed.
        """
        # Obtain the non-initialized class of plugin
        plugin_class = plugin if isinstance(plugin, type) else plugin.__class__

        if connected_plugin := self._search_connected_plugin(plugin_class):
            try:
                connected_plugin.teardown()
            finally:
                self.plugins.remove(connected_plugin)
            return True
        return False

    def send_to_plugins(
        self,
        method: Callable[_P, None],
        ignore_missing_method: bool = False,
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> bool:
        """Call a given method for all connected plugins.

        Parameters
        ----------
        method : Callable[_P, None]
            The method to call.
        ignore_missing_method : bool
            If :py:exc:`NotImplementedError` should be raised, see the ``Raises`` part.
        *args : _P.args
            The arguments to pass.
        **kwargs : _P.kwargs
            The positional arguments to pass.

        Raises
        ------
        :py:exc:`NotImplementedError` :
            Raised if ``ignore_missing_method`` is set to ``False`` and that one of the plugins
            does not have defined the method in its class.
        :py:exc:`Exception` :
            Any exception raised by the given method.

        Returns
        -------
        :py:class:`bool` :
            If the function has been called with success.
            Return `False` when the function has raised `NotImplementedError`, else `True`
        """
        to_call = cast(
            List[Callable[_P, None]],
            [getattr(plugin, method.__name__, None) for plugin in self.plugins],
        )

        if (not ignore_missing_method) and any(func is None for func in to_call):
            raise NotImplementedError(
                f'All plugins does not have the "{str(method)}" method defined.'
            )

        for func in to_call:
            try:
                func(*args, **kwargs)
            except NotImplementedError:
                return False
        return True


class Singleton:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
