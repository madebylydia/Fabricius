import pathlib

from fabricius.exceptions.base import FabriciusException


class InvalidForgeException(FabriciusException):
    def __init__(self, file: pathlib.Path) -> None:
        super().__init__(f"{file.resolve()} is not a valid forge.")
