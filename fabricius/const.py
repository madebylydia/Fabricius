import os
import pathlib
import typing

from rich.theme import Theme

TerminalTheme = Theme(
    {
        "fabricius.error": "black on bright_red",
        "fabricius.warning.box": "white on yellow",
        "fabricius.warning": "yellow",
        "fabricius.success.box": "white on bright_green",
        "fabricius.success": "bright_green",
        "fabricius.skip.box": "white on bright_blue",
        "fabricius.skip": "bright_blue",
        "fabricius.overwrite.box": "white on bright_cyan",
        "fabricius.overwrite": "bright_cyan",
        "fabricius.title": "white on cyan",
        "fabricius.input": "magenta",
    },
)


Data: typing.TypeAlias = typing.Dict[str, typing.Any]
"""
Represent the data passed to a generator/file, under a form of dictionary.
"""

FILE_STATE = typing.Literal["pending", "persisted", "deleted"]
"""
Define the state of a file.

The file's state can be one of:

* pending
* persisted
* deleted
"""

PathStrOrPath = str | os.PathLike[str] | pathlib.Path
"""
Represent a path as a :py:class:`str` or a :py:class:`pathlib.Path` object.
Typically what's used to treat path in Fabricius.
"""
