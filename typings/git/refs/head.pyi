from typing import Any, Sequence, Union

from _typeshed import Incomplete
from git.config import GitConfigParser, SectionConstraint
from git.refs import RemoteReference
from git.repo import Repo
from git.types import Commit_ish, PathLike

from .reference import Reference
from .symbolic import SymbolicReference

class HEAD(SymbolicReference):
    commit: Incomplete
    def __init__(self, repo: Repo, path: PathLike = ...) -> None: ...
    def orig_head(self) -> SymbolicReference: ...
    def reset(
        self,
        commit: Union[Commit_ish, SymbolicReference, str] = ...,
        index: bool = ...,
        working_tree: bool = ...,
        paths: Union[PathLike, Sequence[PathLike], None] = ...,
        **kwargs: Any,
    ) -> HEAD: ...

class Head(Reference):
    k_config_remote: str
    k_config_remote_ref: str
    @classmethod
    def delete(
        cls, repo: Repo, *heads: Union[Head, str], force: bool = ..., **kwargs: Any
    ) -> None: ...
    def set_tracking_branch(self, remote_reference: Union["RemoteReference", None]) -> Head: ...
    def tracking_branch(self) -> Union["RemoteReference", None]: ...
    path: Incomplete
    def rename(self, new_path: PathLike, force: bool = ...) -> Head: ...
    def checkout(self, force: bool = ..., **kwargs: Any) -> Union["HEAD", "Head"]: ...
    def config_reader(self) -> SectionConstraint[GitConfigParser]: ...
    def config_writer(self) -> SectionConstraint[GitConfigParser]: ...
