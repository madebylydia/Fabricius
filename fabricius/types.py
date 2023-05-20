import pathlib
import typing

if typing.TYPE_CHECKING:
    import os

Data: typing.TypeAlias = "dict[str, typing.Any]"
"""
Data is an alias that represents a dictionary of which every keys are string and their values
of any types.
"""

PathStrOrPath: typing.TypeAlias = "str | os.PathLike[str] | pathlib.Path"
"""
PathStrOrPath represents a path as a :py:class:`str` or a :py:class:`pathlib.Path` object.
Used to help users either have an easy way to give their path.
"""

FILE_STATE = typing.Literal["pending", "persisted"]


class FileCommitResult(typing.TypedDict):
    """
    A FileCommitResult is returned when a file was successfully saved.
    It returns its information after its creation.
    """

    name: str
    """
    The name of the file.
    """

    state: FILE_STATE
    """
    The state of the file. Should always be "persisted".
    """

    destination: pathlib.Path
    """
    Where the file is located/has been saved.
    """

    data: Data
    """
    The data that has been passed during rendering.
    """

    template_content: str
    """
    The original content of the template.
    """

    content: str
    """
    The resulting content of the saved file.
    """

    fake: bool
    """
    If the file was faked.
    If faked, the file has not been saved to the disk.
    """
