from fabricius.exceptions.base import FabriciusException


class UserInputException(FabriciusException):
    """
    Raised when user's input cannot be processed as intended.
    """

    def __init__(self, original: str, expected: str) -> None:
        super().__init__(
            f'Cannot process user\'s input, received "{original}", expected "{expected}".'
        )
