import typing

from fabricius.exceptions.commit_exception.base import CommitException
from fabricius.types import PathLike


class MissingPermissions(CommitException, PermissionError):
    """Base class for all exceptions related to commiting, which allow for more conscise exceptions."""

    def __init__(
        self,
        object_of_exception: object,
        at_path: PathLike,
        *has_expected: typing.Literal["read", "write", "execute"],
    ) -> None:
        super().__init__(
            f"{object_of_exception} missing permissions at {at_path}, expected {', '.join(has_expected)} permission(s)."
        )
