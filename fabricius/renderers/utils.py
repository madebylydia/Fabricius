import typing


class DictAllowMiss(typing.Dict[str, typing.Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with renderer.

    :meta private:
    """

    def __missing__(self, _: str) -> typing.Literal[""]:
        return ""
