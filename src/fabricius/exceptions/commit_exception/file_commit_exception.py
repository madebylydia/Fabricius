import enum
import typing

from fabricius.exceptions import PreconditionException
from fabricius.exceptions.commit_exception.base import CommitException

if typing.TYPE_CHECKING:
    from fabricius.models.file import File


class ErrorReason(enum.StrEnum):
    """A list (enum) of possible reasons for a file to fail to be committed."""

    ALREADY_EXIST = "File {} already exist on disk."
    ALREADY_PERSISTED = "File {} is already persisted and cannot be re-committed."
    ALREADY_DELETED = "File {} is already deleted and cannot be re-committed."
    IS_PENDING = "File {} is pending and cannot be committed."
    FAILED = "File {} failed to be committed. Create a new File instance to retry."


class FileCommitException(CommitException):
    """An exception raised when a file has failed to be committed."""

    def __init__(self, file: "File", error_reason: ErrorReason) -> None:
        try:
            destination = str(file.compute_destination())
        except PreconditionException:
            destination = file.name
        super().__init__(error_reason.value.format(destination))
