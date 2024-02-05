import typing

if typing.TYPE_CHECKING:
    import os
    import pathlib


MutableData: typing.TypeAlias = typing.MutableMapping[str, typing.Any]
Data: typing.TypeAlias = typing.Mapping[str, typing.Any]
Extra: typing.TypeAlias = typing.Mapping[str, typing.Any]

NoExtraDict = typing.TypedDict("NoExtraDict", {})

PathLike: typing.TypeAlias = "str | os.PathLike[str] | pathlib.Path"
