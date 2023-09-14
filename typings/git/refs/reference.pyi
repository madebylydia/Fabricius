from typing import Any, Iterator, Union

from _typeshed import Incomplete
from git.repo import Repo
from git.types import Commit_ish, PathLike
from git.util import IterableObj, LazyMixin

from .symbolic import SymbolicReference, T_References

class Reference(SymbolicReference, LazyMixin, IterableObj):
    path: Incomplete
    def __init__(self, repo: Repo, path: PathLike, check_path: bool = ...) -> None: ...
    def set_object(
        self, object: Union[Commit_ish, "SymbolicReference", str], logmsg: Union[str, None] = ...
    ) -> Reference: ...
    @property
    def name(self) -> str: ...
    @classmethod
    def iter_items(
        cls, repo: Repo, common_path: Union[PathLike, None] = ..., *args: Any, **kwargs: Any
    ) -> Iterator[T_References]: ...
    @property
    def remote_name(self) -> str: ...
    @property
    def remote_head(self) -> str: ...
