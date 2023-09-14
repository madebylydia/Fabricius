from fabricius.exceptions.base import FabriciusException


class PreconditionException(FabriciusException):
    def __init__(self, object_of_precondition: object, condition: str) -> None:
        super().__init__(
            f"Class {object_of_precondition.__class__.__name__} require the following "
            f"precondition: {condition}"
        )
