from typing import Any, Union

from git.objects import Commit, TagObject
from git.refs import SymbolicReference
from git.repo import Repo
from git.types import Commit_ish, PathLike

from .reference import Reference

class TagReference(Reference):
    @property
    def commit(self) -> Commit: ...
    @property
    def tag(self) -> Union["TagObject", None]: ...
    @property
    def object(self) -> Commit_ish: ...
    @classmethod
    def create(
        cls,
        repo: Repo,
        path: PathLike,
        reference: Union[str, "SymbolicReference"] = ...,
        logmsg: Union[str, None] = ...,
        force: bool = ...,
        **kwargs: Any
    ) -> TagReference: ...
    @classmethod
    def delete(cls, repo: Repo, *tags: TagReference) -> None: ...

Tag = TagReference
