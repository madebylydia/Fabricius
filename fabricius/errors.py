from typing import Optional


class FabriciusError(Exception):
    """
    An error was raised inside Fabricius.
    """

    def __init__(self, error: Optional[object] = None) -> None:
        """
        An error was raised inside Fabricius.
        """
        super().__init__(error or "Error inside Fabricius. No specific error raised.")


class PluginConnectionError(FabriciusError):
    """
    There was an error while trying to connect the plugin
    """

    def __init__(self, plugin_name: str, reason: str) -> None:
        super().__init__(f"Plugin '{plugin_name}' could not be connected: {reason}")
