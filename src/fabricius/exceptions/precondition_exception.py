from fabricius.exceptions.base import FabriciusException


class PreconditionException(FabriciusException):
    """Raised at runtime when a condition that was expected to be met was not.

    This exception is very often used to make sure that everything is in order before executing
    anything persistent, like committing a file.
    """

    def __init__(self, object_of_precondition: object, condition: str) -> None:
        super().__init__(
            f"Class {object_of_precondition.__class__.__name__} require the following "
            f"precondition: {condition}"
        )
