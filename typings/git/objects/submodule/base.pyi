from typing import Any, Iterator, Mapping, Sequence, Union

from _typeshed import Incomplete
from git.config import SectionConstraint
from git.index import IndexFile
from git.objects.base import IndexObject
from git.objects.util import TraversableIterableObj
from git.refs import Head
from git.repo import Repo
from git.types import TBD, Commit_ish, Literal, PathLike
from git.util import IterableList, RemoteProgress

from .util import SubmoduleConfigParser

class UpdateProgress(RemoteProgress):
    CLONE: Incomplete
    FETCH: Incomplete
    UPDWKTREE: Incomplete

class Submodule(IndexObject, TraversableIterableObj):
    k_modules_file: str
    k_head_option: str
    k_head_default: str
    k_default_mode: Incomplete
    type: Literal["submodule"]
    size: int
    def __init__(
        self,
        repo: Repo,
        binsha: bytes,
        mode: Union[int, None] = ...,
        path: Union[PathLike, None] = ...,
        name: Union[str, None] = ...,
        parent_commit: Union[Commit_ish, None] = ...,
        url: Union[str, None] = ...,
        branch_path: Union[PathLike, None] = ...,
    ) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    @classmethod
    def add(
        cls,
        repo: Repo,
        name: str,
        path: PathLike,
        url: Union[str, None] = ...,
        branch: Union[str, None] = ...,
        no_checkout: bool = ...,
        depth: Union[int, None] = ...,
        env: Union[Mapping[str, str], None] = ...,
        clone_multi_options: Union[Sequence[TBD], None] = ...,
        allow_unsafe_options: bool = ...,
        allow_unsafe_protocols: bool = ...,
    ) -> Submodule: ...
    def update(
        self,
        recursive: bool = ...,
        init: bool = ...,
        to_latest_revision: bool = ...,
        progress: Union["UpdateProgress", None] = ...,
        dry_run: bool = ...,
        force: bool = ...,
        keep_going: bool = ...,
        env: Union[Mapping[str, str], None] = ...,
        clone_multi_options: Union[Sequence[TBD], None] = ...,
        allow_unsafe_options: bool = ...,
        allow_unsafe_protocols: bool = ...,
    ) -> Submodule: ...
    path: Incomplete
    def move(
        self, module_path: PathLike, configuration: bool = ..., module: bool = ...
    ) -> Submodule: ...
    def remove(
        self, module: bool = ..., force: bool = ..., configuration: bool = ..., dry_run: bool = ...
    ) -> Submodule: ...
    binsha: Incomplete
    def set_parent_commit(
        self, commit: Union[Commit_ish, None], check: bool = ...
    ) -> Submodule: ...
    def config_writer(
        self, index: Union["IndexFile", None] = ..., write: bool = ...
    ) -> SectionConstraint["SubmoduleConfigParser"]: ...
    def rename(self, new_name: str) -> Submodule: ...
    def module(self) -> Repo: ...
    def module_exists(self) -> bool: ...
    def exists(self) -> bool: ...
    @property
    def branch(self) -> Head: ...
    @property
    def branch_path(self) -> PathLike: ...
    @property
    def branch_name(self) -> str: ...
    @property
    def url(self) -> str: ...
    @property
    def parent_commit(self) -> Commit_ish: ...
    @property
    def name(self) -> str: ...
    def config_reader(self) -> SectionConstraint[SubmoduleConfigParser]: ...
    def children(self) -> IterableList["Submodule"]: ...
    @classmethod
    def iter_items(
        cls, repo: Repo, parent_commit: Union[Commit_ish, str] = ..., *Args: Any, **kwargs: Any
    ) -> Iterator["Submodule"]: ...
