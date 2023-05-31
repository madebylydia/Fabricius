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
