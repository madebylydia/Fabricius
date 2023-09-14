from fabricius.exceptions.base import FabriciusException


class ExpectationFailedException(FabriciusException):
    """
    An exception raised when the function was expecting something in particular, but was not met.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(f"Expectation failed: {reason}")
