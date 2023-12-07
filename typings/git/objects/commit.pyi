import datetime
from typing import Any, Dict, Iterator, List, Sequence, Union

from _typeshed import Incomplete
from git.diff import Diffable
from git.refs import SymbolicReference
from git.repo import Repo
from git.types import Literal, PathLike
from git.util import Actor, Stats

from . import base
from .tree import Tree
from .util import Serializable, TraversableIterableObj

class Commit(base.Object, TraversableIterableObj, Diffable, Serializable):
    env_author_date: str
    env_committer_date: str
    conf_encoding: str
    default_encoding: str
    type: Literal["commit"]
    binsha: Incomplete
    tree: Incomplete
    author: Incomplete
    authored_date: Incomplete
    author_tz_offset: Incomplete
    committer: Incomplete
    committed_date: Incomplete
    committer_tz_offset: Incomplete
    message: Incomplete
    parents: Incomplete
    encoding: Incomplete
    gpgsig: Incomplete
    def __init__(
        self,
        repo: Repo,
        binsha: bytes,
        tree: Union[Tree, None] = ...,
        author: Union[Actor, None] = ...,
        authored_date: Union[int, None] = ...,
        author_tz_offset: Union[None, float] = ...,
        committer: Union[Actor, None] = ...,
        committed_date: Union[int, None] = ...,
        committer_tz_offset: Union[None, float] = ...,
        message: Union[str, bytes, None] = ...,
        parents: Union[Sequence["Commit"], None] = ...,
        encoding: Union[str, None] = ...,
        gpgsig: Union[str, None] = ...,
    ) -> None: ...
    def replace(self, **kwargs: Any) -> Commit: ...
    @property
    def authored_datetime(self) -> datetime.datetime: ...
    @property
    def committed_datetime(self) -> datetime.datetime: ...
    @property
    def summary(self) -> Union[str, bytes]: ...
    def count(self, paths: Union[PathLike, Sequence[PathLike]] = ..., **kwargs: Any) -> int: ...
    @property
    def name_rev(self) -> str: ...
    @classmethod
    def iter_items(
        cls,
        repo: Repo,
        rev: Union[str, "Commit", "SymbolicReference"],
        paths: Union[PathLike, Sequence[PathLike]] = ...,
        **kwargs: Any,
    ) -> Iterator["Commit"]: ...
    def iter_parents(
        self, paths: Union[PathLike, Sequence[PathLike]] = ..., **kwargs: Any
    ) -> Iterator["Commit"]: ...
    @property
    def stats(self) -> Stats: ...
    @property
    def trailers(self) -> Dict: ...
    @classmethod
    def create_from_tree(
        cls,
        repo: Repo,
        tree: Union[Tree, str],
        message: str,
        parent_commits: Union[None, List["Commit"]] = ...,
        head: bool = ...,
        author: Union[None, Actor] = ...,
        committer: Union[None, Actor] = ...,
        author_date: Union[None, str, datetime.datetime] = ...,
        commit_date: Union[None, str, datetime.datetime] = ...,
    ) -> Commit: ...
    @property
    def co_authors(self) -> List[Actor]: ...
