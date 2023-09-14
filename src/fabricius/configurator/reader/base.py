import abc
import pathlib
import typing

if typing.TYPE_CHECKING:
    from fabricius.configurator.universal import UniversalConfig


_PD = typing.TypeVar("_PD")
"""The return type of the parsed data."""


class BaseReader(abc.ABC, typing.Generic[_PD]):
    config_file: pathlib.Path

    def __init__(self, file: pathlib.Path) -> None:
        self.config_file = file

    @abc.abstractmethod
    def process(self) -> _PD:
        """
        Process the raw content of a file so it can be analyzed by the :py:meth:`.to_universal`
        method.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def to_universal(self, parsed_data: _PD) -> "UniversalConfig":
        """
        An abstract class that must return an
        :py:class:`fabricius.configurator.universal.UniversalConfig` class.

        Parameters
        ----------
        parsed_data : Any
            The parsed data by the :py:meth:`.process` method.

        Returns
        -------
        :py:class:`fabricius.configurator.universal.UniversalConfig` :
            The parsed data under the form of UniversalConfig.
        """
        raise NotImplementedError()
