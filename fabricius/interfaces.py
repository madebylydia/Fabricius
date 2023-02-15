import typing

from typing_extensions import Self


class Singleton(object):
    _instance = None

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
