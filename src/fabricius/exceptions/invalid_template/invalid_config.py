import pathlib
import typing

from fabricius.configurator.reader.base import BaseReader
from fabricius.exceptions.invalid_template.base import InvalidTemplateException


class InvalidConfigException(InvalidTemplateException):
    """
    Raised when the config file is invalid.
    """

    def __init__(
        self, file: pathlib.Path, reader: type[BaseReader[typing.Any, typing.Any]], reason: str
    ) -> None:
        super().__init__(
            f"Could not read config file ({file}) using {reader.__class__.__name__}: {reason}"
        )
