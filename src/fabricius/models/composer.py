import abc
import typing

from fabricius.types import Data


class Composer(abc.ABC):
    """The Composer is what translate and generates the output of templates. Core of the work.

    You must subclass this class and override the :py:meth:`render` method, if possible, also add
    a name.
    """

    name: typing.ClassVar[str | None] = None
    """The name of the composer, not necessary, but suggested to add."""

    data: Data
    """A dictionary that contains data passed by the users to pass inside the template."""

    def __init__(self) -> None:
        self.data = {}

    def push_data(self, data: Data) -> typing.Self:
        """Push data into the composer.
        Overwrites the previous data.

        Parameters
        ----------
        data : :py:class:`dict`
            The data to push.
        """
        self.data = data
        return self

    @abc.abstractmethod
    def render(self, content: str) -> str:
        """This method will process a given string, the template input and return the processed
        template as a string too.

        Parameters
        ----------
        content : :py:class:`str`
            The template.

        Returns
        -------
        :py:class:`str` :
            The result of the processed template.
        """
        raise NotImplementedError()
