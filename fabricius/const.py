import os
import pathlib
from typing import Any, Dict, Literal, TypeAlias


class Colors:
    """
    An Enum indicating which colors to use with the Rich's console.

    You may create your own Colors class by subclassing this class and overwriting the constants.

    Example
    -------

    class MyColors(fabricius.const.Colors):
        ERROR = "red"
        WARNING = "yellow"

        # The others colors are untouched.
    """
    ERROR = "bright_red"
    WARNING = "yellow"

    SUCCESS = "bright_green"
    SKIP = "bright_blue"
    OVERWRITE = "bright_cyan"

    TITLE = "cyan"
    INPUT = "magenta"


Data: TypeAlias = Dict[str, Any]
"""
Represent the data passed to a generator/file, under a form of dictionary.
"""

FILE_STATE = Literal["pending", "persisted", "deleted"]
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
