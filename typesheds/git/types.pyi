import abc
import os
from typing import Any, Dict, NoReturn, TypedDict, Union

from _typeshed import Incomplete
from git.objects import Blob as Blob
from git.objects import Commit as Commit
from git.objects import TagObject as TagObject
from git.objects import Tree as Tree
from git.repo import Repo as Repo

PathLike = Union[str, os.PathLike[str]]
TBD = Any
Tree_ish: Incomplete
Commit_ish: Incomplete
Lit_commit_ish: Incomplete
Lit_config_levels: Incomplete
ConfigLevels_Tup: Incomplete

def assert_never(
    inp: NoReturn, raise_error: bool = ..., exc: Union[Exception, None] = ...
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

class Has_Repo(metaclass=abc.ABCMeta):
    repo: Repo

class Has_id_attribute(metaclass=abc.ABCMeta): ...
