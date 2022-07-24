from typing import Any, Dict, Literal, TypeAlias

Data: TypeAlias = Dict[str, Any]
"""
Represent the data passed to a generator/file, under a form of dictionary.
"""

FILE_STATE = Literal["pending", "persisted", "deleted"]
"""
Define the state of a file.

The file's state can be one of:

* pending
* persisted
* deleted
"""
