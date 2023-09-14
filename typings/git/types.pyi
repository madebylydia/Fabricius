# -*- coding: utf-8 -*-
# This module is part of GitPython and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php
# flake8: noqa

import os
import sys
from typing import (  # noqa: F401
    Any,
    Dict,
    Literal,
    NoReturn,
    Protocol,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
    runtime_checkable,
)

# if sys.version_info[:2] >= (3, 10):
#     from typing import TypeGuard  # noqa: F401
# else:
#     from typing_extensions import TypeGuard  # noqa: F401

PathLike = Union[str, os.PathLike[str]]

TBD = Any
_T = TypeVar("_T")

Tree_ish = Literal["Commit", "Tree"]
Commit_ish = Literal["Commit", "TagObject", "Blob", "Tree"]
Lit_commit_ish = Literal["commit", "tag", "blob", "tree"]

# Config_levels ---------------------------------------------------------

Lit_config_levels = Literal["system", "global", "user", "repository"]

# def is_config_level(inp: str) -> TypeGuard[Lit_config_levels]:
#     # return inp in get_args(Lit_config_level)  # only py >= 3.8
#     return inp in ("system", "user", "global", "repository")

ConfigLevels_Tup = Tuple[
    Literal["system"], Literal["user"], Literal["global"], Literal["repository"]
]

# -----------------------------------------------------------------------------------

def assert_never(
    inp: NoReturn, raise_error: bool = True, exc: Union[Exception, None] = None
) -> None: ...

class Files_TD(TypedDict):
    insertions: int
    deletions: int
    lines: int

class Total_TD(TypedDict):
    insertions: int
    deletions: int
    lines: int
    files: int

class HSH_TD(TypedDict):
    total: Total_TD
    files: Dict[PathLike, Files_TD]

@runtime_checkable
class Has_Repo(Protocol):
    repo: Literal["Repo"]

@runtime_checkable
class Has_id_attribute(Protocol):
    _id_attribute_: str
