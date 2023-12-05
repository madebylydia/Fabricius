import sys
import typing

from rich import get_console

from fabricius.exceptions.base import FabriciusError


class UserFeedbackError(FabriciusError):
    """
    Exception raised to show a user-friendly message.

    This exception is used to display a message to the user without showing the traceback.
    It is intended to provide helpful information or instructions to the user when an error occurs.
    """

    message: str
    """
    The message to print to the user.
    """

    def __init__(self, message: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.message = message
        super().__init__(message, *args, **kwargs)

    def handle(self, exit_code: int = 0, **kwargs: typing.Any) -> typing.NoReturn:
        get_console().print(kwargs["traceback"])
        sys.exit(exit_code)
