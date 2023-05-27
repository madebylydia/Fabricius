import contextlib
import typing

_F = typing.ParamSpec("_F")


class Signal(typing.Generic[_F]):
    """
    The Listener is the base class used to create listeners of events.
    """

    listeners: list[typing.Callable[_F, typing.Any]]
    """
    The list of listeners that are subscribed to this signal.
    """

    def __init__(self, *, func_hint: typing.Callable[_F, typing.Any] | None = None) -> None:
        self.listeners = []

    def connect(self, listener: typing.Callable[_F, typing.Any]) -> None:
        """
        Connect a listener to this signal.
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def disconnect(self, listener: typing.Callable[_F, typing.Any]) -> None:
        """
        Disconnect a listener to this signal.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    def send(self, *args: _F.args, **kwargs: _F.kwargs) -> list[typing.Any]:
        """
        Sends the signal to all subscribed listeners.
        """
        results: list[typing.Any] = []
        for listener in self.listeners:
            with contextlib.suppress(NotImplementedError):
                result = listener(*args, **kwargs)
                results.append(result)
        return results
