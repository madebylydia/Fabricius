import typing

_F = typing.ParamSpec("_F")


class Signal(typing.Generic[_F]):
    """
    The Listener is the base class used to create listeners of events.
    """

    listeners: list[typing.Callable[..., typing.Any]]
    """
    The list of listeners that are subscribed to this signal.
    """

    def __init__(self, *, func_hint: typing.Callable[_F, typing.Any] | None = None) -> None:
        self.listeners = []

    def connect(self, listener: typing.Callable[_F, typing.Any]) -> None:
        """
        Connects a listener to this signal.
        """
        self.listeners.append(listener)

    def send(self, *args: _F.args, **kwargs: _F.kwargs) -> list[typing.Any]:
        """
        Sends the signal to all subscribed listeners.
        """
        results: list[typing.Any] = []
        for listener in self.listeners:
            try:
                result = listener(*args, **kwargs)
                results.append(result)
            except NotImplementedError:
                pass
            except Exception as e:
                results.append(e)
        return results
