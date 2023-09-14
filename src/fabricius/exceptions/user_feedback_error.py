import sys
import typing

from rich import get_console

from fabricius.exceptions.base import FabriciusError


class UserFeedbackError(FabriciusError):
    """
    Raised when an error should print to the console a message.
    """

    message: str
    """
    The message to print to the user.
    """

    def __init__(self, message: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.message = message
        super().__init__(message, *args, **kwargs)

    def handle(self, exit_code: int = 0, **kwargs: typing.Any) -> typing.NoReturn:
        get_console().print(self.message)
        sys.exit(exit_code)
