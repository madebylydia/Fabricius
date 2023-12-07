import datetime
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Sequence,
    Tuple,
    Type,
    Union,
)

import git.diff as git_diff
from _typeshed import Incomplete
from git.exc import CheckoutError as CheckoutError
from git.objects import Blob, Commit, Submodule, Tree
from git.objects.util import Serializable
from git.refs.reference import Reference
from git.repo import Repo
from git.types import Commit_ish, PathLike
from git.util import Actor, LazyMixin

from .fun import S_IFGITLINK
from .typ import BaseIndexEntry
from .typ import StageType as StageType

Treeish = Union[Tree, Commit, str, bytes]

class IndexFile(LazyMixin, git_diff.Diffable, Serializable):
    S_IFGITLINK = S_IFGITLINK
    repo: Incomplete
    version: Incomplete
    def __init__(self, repo: Repo, file_path: Union[PathLike, None] = ...) -> None: ...
    @property
    def path(self) -> PathLike: ...
    def write(
        self, file_path: Union[None, PathLike] = ..., ignore_extension_data: bool = ...
    ) -> None: ...
    def merge_tree(self, rhs: Treeish, base: Union[None, Treeish] = ...) -> IndexFile: ...
    @classmethod
    def new(cls, repo: Repo, *tree_sha: Union[str, Tree]) -> IndexFile: ...
    @classmethod
    def from_tree(cls, repo: Repo, *treeish: Treeish, **kwargs: Any) -> IndexFile: ...
    def iter_blobs(
        self, predicate: Callable[[Tuple[StageType, Blob]], bool] = ...
    ) -> Iterator[Tuple[StageType, Blob]]: ...
    def unmerged_blobs(self) -> Dict[PathLike, List[Tuple[StageType, Blob]]]: ...
    @classmethod
    def entry_key(
        cls, *entry: Union[BaseIndexEntry, PathLike, StageType]
    ) -> Tuple[PathLike, StageType]: ...
    def resolve_blobs(self, iter_blobs: Iterator[Blob]) -> IndexFile: ...
    def update(self) -> IndexFile: ...
    def write_tree(self) -> Tree: ...
    def add(
        self,
        items: Sequence[Union[PathLike, Blob, BaseIndexEntry, "Submodule"]],
        force: bool = ...,
        fprogress: Callable = ...,
        path_rewriter: Union[Callable[..., PathLike], None] = ...,
        write: bool = ...,
        write_extension_data: bool = ...,
    ) -> List[BaseIndexEntry]: ...
    def remove(
        self,
        items: Sequence[Union[PathLike, Blob, BaseIndexEntry, "Submodule"]],
        working_tree: bool = ...,
        **kwargs: Any,
    ) -> List[str]: ...
    def move(
        self,
        items: Sequence[Union[PathLike, Blob, BaseIndexEntry, "Submodule"]],
        skip_errors: bool = ...,
        **kwargs: Any,
    ) -> List[Tuple[str, str]]: ...
    def commit(
        self,
        message: str,
        parent_commits: Union[Commit_ish, None] = ...,
        head: bool = ...,
        author: Union[None, "Actor"] = ...,
        committer: Union[None, "Actor"] = ...,
        author_date: Union[datetime.datetime, str, None] = ...,
        commit_date: Union[datetime.datetime, str, None] = ...,
        skip_hooks: bool = ...,
    ) -> Commit: ...
    def checkout(
        self,
        paths: Union[None, Iterable[PathLike]] = ...,
        force: bool = ...,
        fprogress: Callable = ...,
        **kwargs: Any,
    ) -> Union[None, Iterator[PathLike], Sequence[PathLike]]: ...
    entries: Incomplete
    def reset(
        self,
        commit: Union[Commit, "Reference", str] = ...,
        working_tree: bool = ...,
        paths: Union[None, Iterable[PathLike]] = ...,
        head: bool = ...,
        **kwargs: Any,
    ) -> IndexFile: ...
    def diff(
        self,
        other: Union[Type["git_diff.Diffable.Index"], "Tree", "Commit", str, None] = ...,
        paths: Union[PathLike, List[PathLike], Tuple[PathLike, ...], None] = ...,
        create_patch: bool = ...,
        **kwargs: Any,
    ) -> git_diff.DiffIndex: ...
