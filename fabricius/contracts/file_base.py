from abc import ABC

from fabricius.const import FILE_STATE


class BaseFile(ABC):
    """
    Base class for files, not much of a contract, but contain 2 important properties.

    .. property:: name

       The name of the file.

       :type: str

    .. property:: state

       The state of the file.

       :type: :py:data:`.FILE_STATE`
    """

    name: str
    state: FILE_STATE
