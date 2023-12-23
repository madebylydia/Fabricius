from fabricius.exceptions.base import FabriciusException


class CommitException(FabriciusException):
    """Base class for all exceptions related to commiting, which allow for more conscise exceptions."""
