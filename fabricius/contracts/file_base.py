from abc import ABC

from fabricius.const import FILE_STATE


class BaseFileContract(ABC):
    """
    Base class for files, not much of a contract, but contain 2 important properties.
    """

    name: str
    """
    The name of the file.
    """

    state: FILE_STATE
    """
    The state of the file.
    """
