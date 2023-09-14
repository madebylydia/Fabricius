import typing

from aspreno import ArgumentedException


class FabriciusException(Exception):
    """
    An exception was raised inside Fabricius.

    All exceptions of Fabricius MUST subclass this exception.
    """

    def __init__(self, error: object | None = None) -> None:
        super().__init__(error or "Exception inside Fabricius. No specific error raised.")


class FabriciusError(ArgumentedException):
    """
    An error was raised inside Fabricius.

    All errors of Fabricius MUST subclass this exception.

    The difference between an exception and an error is that an error might prevent the application
    from continuing its normal workflow, and might exit when possible.
    """

    def __init__(
        self, error: object | None = None, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        super().__init__(
            error or "Error inside Fabricius. No specific error raised.", *args, **kwargs
        )
