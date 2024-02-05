import typing

from fabricius.exceptions.commit_exception.base import CommitException

if typing.TYPE_CHECKING:
    from fabricius.models.file import File
    from fabricius.types import PathLike


class MissingPermissions(CommitException, PermissionError):
    """Base class for all exceptions related to commiting, which allow for more conscise
    exceptions.
    """

    def __init__(
        self,
        file: "File",
        at_path: "PathLike",
        *has_expected: typing.Literal["read", "write", "execute"],
    ) -> None:
        super().__init__(
            f"{file} is missing permissions at {at_path}, expected "
            f"{', '.join(has_expected)} permission(s)."
        )
