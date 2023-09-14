from typing import Any, Union

from _typeshed import Incomplete
from git.refs.reference import Reference
from git.repo import Repo
from git.types import Commit_ish, Lit_commit_ish, PathLike
from git.util import LazyMixin
from gitdb.base import OStream

class Object(LazyMixin):
    NULL_HEX_SHA: Incomplete
    NULL_BIN_SHA: Incomplete
    TYPES: Incomplete
    type: Union[Lit_commit_ish, None]
    repo: Incomplete
    binsha: Incomplete
    def __init__(self, repo: Repo, binsha: bytes) -> None: ...
    @classmethod
    def new(cls, repo: Repo, id: Union[str, "Reference"]) -> Commit_ish: ...
    @classmethod
    def new_from_sha(cls, repo: Repo, sha1: bytes) -> Commit_ish: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    @property
    def hexsha(self) -> str: ...
    @property
    def data_stream(self) -> OStream: ...
    def stream_data(self, ostream: OStream) -> Object: ...

class IndexObject(Object):
    mode: Incomplete
    path: Incomplete
    def __init__(
        self,
        repo: Repo,
        binsha: bytes,
        mode: Union[None, int] = ...,
        path: Union[None, PathLike] = ...,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def abspath(self) -> PathLike: ...
