import enum
import typing

from fabricius.exceptions.base import FabriciusException
from fabricius.exceptions.precondition_exception import PreconditionException

if typing.TYPE_CHECKING:
    from fabricius.models.file import File


class ErrorReason(enum.StrEnum):
    ALREADY_EXIST = "File {} already exist on disk."
    ALREADY_PERSISTED = "File {} is already persisted and cannot be re-committed."


class FileCommitException(FabriciusException):
    def __init__(self, file: "File", error_reason: ErrorReason) -> None:
        try:
            destination = str(file.compute_destination())
        except PreconditionException:
            destination = file.name
        super().__init__(error_reason.value.format(destination))
