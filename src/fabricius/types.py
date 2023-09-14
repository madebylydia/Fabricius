import typing

if typing.TYPE_CHECKING:
    import os
    import pathlib


Data = typing.NewType("Data", dict[str, typing.Any])

PathLike: typing.TypeAlias = "str | os.PathLike[str] | pathlib.Path"
