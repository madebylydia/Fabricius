import abc
import pathlib
import typing

if typing.TYPE_CHECKING:
    from fabricius.configurator.universal import UniversalConfig
    from fabricius.types import Extra


class BaseReader[ParsedData: typing.Any, Extra: "Extra"](abc.ABC):
    """The base class for all file readers to implement.

    This consists of two methods that must be implemented by the child class:
    :py:meth:`.process` and :py:meth:`.universalize`.

    The :py:meth:`.process` method is responsible for processing the raw content of a file that
    will be given to the :py:meth:`.universalize` method.
    The :py:meth:`.universalize` method is responsible for returning the parsed data under the form
    of a :py:class:`fabricius.configurator.universal.UniversalConfig` class.
    """

    config_file: pathlib.Path

    def __init__(self, file: pathlib.Path) -> None:
        self.config_file = file

    @abc.abstractmethod
    def process(self) -> ParsedData:
        """Process the raw content of a file so it can be analyzed by the :py:meth:`.to_universal`
        method.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def universalize(self, parsed_data: ParsedData) -> "UniversalConfig[Extra]":
        """An abstract class that must return an
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

    def obtain(self):
        """Obtain the UniversalConfig from the reader.

        Returns
        -------
        :py:class:`fabricius.configurator.universal.UniversalConfig` :
            The parsed data under the form of UniversalConfig.
        """
        return self.universalize(self.process())
