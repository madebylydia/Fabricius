import collections.abc
import typing

if typing.TYPE_CHECKING:
    import os
    import pathlib


MutableData: typing.TypeAlias = collections.abc.MutableMapping[str, typing.Any]
Data: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
Extra: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]

NoExtraDict = typing.TypedDict("NoExtraDict", {})

PathLike: typing.TypeAlias = "str | os.PathLike[str] | pathlib.Path"
