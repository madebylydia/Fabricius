from typing import Any, Callable, Iterator, List, NoReturn, Optional, Union, overload

from _typeshed import Incomplete
from git.config import GitConfigParser, SectionConstraint
from git.objects.submodule.base import UpdateProgress
from git.refs import Reference, RemoteReference, SymbolicReference, TagReference
from git.repo.base import Repo
from git.types import Commit_ish, Literal, PathLike
from git.util import IterableList, IterableObj, LazyMixin
from git.util import RemoteProgress as RemoteProgress

class PushInfo(IterableObj):
    NEW_TAG: Incomplete
    NEW_HEAD: Incomplete
    NO_MATCH: Incomplete
    REJECTED: Incomplete
    REMOTE_REJECTED: Incomplete
    REMOTE_FAILURE: Incomplete
    DELETED: Incomplete
    FORCED_UPDATE: Incomplete
    FAST_FORWARD: Incomplete
    UP_TO_DATE: Incomplete
    ERROR: Incomplete
    flags: Incomplete
    local_ref: Incomplete
    remote_ref_string: Incomplete
    summary: Incomplete
    def __init__(
        self,
        flags: int,
        local_ref: Union[SymbolicReference, None],
        remote_ref_string: str,
        remote: Remote,
        old_commit: Optional[str] = ...,
        summary: str = ...,
    ) -> None: ...
    @property
    def old_commit(self) -> Union[str, SymbolicReference, Commit_ish, None]: ...
    @property
    def remote_ref(self) -> Union[RemoteReference, TagReference]: ...
    @classmethod
    def iter_items(cls, repo: Repo, *args: Any, **kwargs: Any) -> NoReturn: ...

class PushInfoList(IterableList[PushInfo]):
    def __new__(cls) -> PushInfoList: ...
    error: Incomplete
    def __init__(self) -> None: ...
    def raise_if_error(self) -> None: ...

class FetchInfo(IterableObj):
    NEW_TAG: Incomplete
    NEW_HEAD: Incomplete
    HEAD_UPTODATE: Incomplete
    TAG_UPDATE: Incomplete
    REJECTED: Incomplete
    FORCED_UPDATE: Incomplete
    FAST_FORWARD: Incomplete
    ERROR: Incomplete
    @classmethod
    def refresh(cls) -> Literal[True]: ...
    ref: Incomplete
    flags: Incomplete
    note: Incomplete
    old_commit: Incomplete
    remote_ref_path: Incomplete
    def __init__(
        self,
        ref: SymbolicReference,
        flags: int,
        note: str = ...,
        old_commit: Union[Commit_ish, None] = ...,
        remote_ref_path: Optional[PathLike] = ...,
    ) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def commit(self) -> Commit_ish: ...
    @classmethod
    def iter_items(cls, repo: Repo, *args: Any, **kwargs: Any) -> NoReturn: ...

class Remote(LazyMixin, IterableObj):
    unsafe_git_fetch_options: Incomplete
    unsafe_git_pull_options: Incomplete
    unsafe_git_push_options: Incomplete
    repo: Incomplete
    name: Incomplete
    url: Incomplete
    def __init__(self, repo: Repo, name: str) -> None: ...
    def __getattr__(self, attr: str) -> Any: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def exists(self) -> bool: ...
    @classmethod
    def iter_items(cls, repo: Repo, *args: Any, **kwargs: Any) -> Iterator["Remote"]: ...
    def set_url(
        self,
        new_url: str,
        old_url: Optional[str] = ...,
        allow_unsafe_protocols: bool = ...,
        **kwargs: Any,
    ) -> Remote: ...
    def add_url(self, url: str, allow_unsafe_protocols: bool = ..., **kwargs: Any) -> Remote: ...
    def delete_url(self, url: str, **kwargs: Any) -> Remote: ...
    @property
    def urls(self) -> Iterator[str]: ...
    @property
    def refs(self) -> IterableList[RemoteReference]: ...
    @property
    def stale_refs(self) -> IterableList[Reference]: ...
    @classmethod
    def create(
        cls, repo: Repo, name: str, url: str, allow_unsafe_protocols: bool = ..., **kwargs: Any
    ) -> Remote: ...
    @classmethod
    def add(cls, repo: Repo, name: str, url: str, **kwargs: Any) -> Remote: ...
    @classmethod
    def remove(cls, repo: Repo, name: str) -> str: ...
    rm = remove
    def rename(self, new_name: str) -> Remote: ...
    def update(self, **kwargs: Any) -> Remote: ...
    def fetch(
        self,
        refspec: Union[str, List[str], None] = ...,
        progress: Union[RemoteProgress, None, "UpdateProgress"] = ...,
        verbose: bool = ...,
        kill_after_timeout: Union[None, float] = ...,
        allow_unsafe_protocols: bool = ...,
        allow_unsafe_options: bool = ...,
        **kwargs: Any,
    ) -> IterableList[FetchInfo]: ...
    def pull(
        self,
        refspec: Union[str, List[str], None] = ...,
        progress: Union[RemoteProgress, "UpdateProgress", None] = ...,
        kill_after_timeout: Union[None, float] = ...,
        allow_unsafe_protocols: bool = ...,
        allow_unsafe_options: bool = ...,
        **kwargs: Any,
    ) -> IterableList[FetchInfo]: ...
    def push(
        self,
        refspec: Union[str, List[str], None] = ...,
        progress: Union[
            RemoteProgress, "UpdateProgress", Callable[..., RemoteProgress], None
        ] = ...,
        kill_after_timeout: Union[None, float] = ...,
        allow_unsafe_protocols: bool = ...,
        allow_unsafe_options: bool = ...,
        **kwargs: Any,
    ) -> PushInfoList: ...
    @property
    def config_reader(self) -> SectionConstraint[GitConfigParser]: ...
    @property
    def config_writer(self) -> SectionConstraint: ...
