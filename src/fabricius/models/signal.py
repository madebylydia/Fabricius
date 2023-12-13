import contextlib
import logging
import typing

_log = logging.getLogger(__name__)


class Signal[**FuncHint]:
    """
    The Listener is the base class used to create listeners of events.
    """

    name: typing.Final[str]
    """
    The name of the signal.
    """

    listeners: list[typing.Callable[FuncHint, typing.Any]]
    """
    The list of listeners that are subscribed to this signal.
    """

    def __init__(
        self, name: str, *, func_hint: typing.Callable[FuncHint, typing.Any] | None = None
    ) -> None:
        self.name = name
        self.listeners = []

    def connect(self, listener: typing.Callable[FuncHint, typing.Any]) -> None:
        """
        Connect a listener to this signal.
        """
        if listener not in self.listeners:
            _log.debug(f"Connecting {listener} to signal {self.name}")
            self.listeners.append(listener)

    def disconnect(self, listener: typing.Callable[FuncHint, typing.Any]) -> None:
        """
        Disconnect a listener to this signal.
        """
        if listener in self.listeners:
            _log.debug(f"Disconnecting {listener} from signal {self.name}")
            self.listeners.remove(listener)

    def send(self, *args: FuncHint.args, **kwargs: FuncHint.kwargs) -> list[typing.Any]:
        """
        Sends the signal to all subscribed listeners.
        """
        results: list[typing.Any] = []
        for listener in self.listeners:
            _log.debug(f"Sending signal {self.name} to {listener}")
            with contextlib.suppress(NotImplementedError):
                result = listener(*args, **kwargs)
                results.append(result)
        return results
