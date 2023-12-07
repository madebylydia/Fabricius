from typing import Any, Iterator, NoReturn, Union

from git import Remote
from git.repo import Repo
from git.types import PathLike

from .head import Head

class RemoteReference(Head):
    @classmethod
    def iter_items(
        cls,
        repo: Repo,
        common_path: Union[PathLike, None] = ...,
        remote: Union["Remote", None] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> Iterator["RemoteReference"]: ...
    @classmethod
    def delete(cls, repo: Repo, *refs: RemoteReference, **kwargs: Any) -> None: ...
    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> NoReturn: ...
