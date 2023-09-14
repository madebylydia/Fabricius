from typing import Union

from _typeshed import Incomplete
from git.repo import Repo
from git.types import Commit_ish

from .base import Submodule, UpdateProgress

class RootUpdateProgress(UpdateProgress):
    REMOVE: Incomplete
    PATHCHANGE: Incomplete
    BRANCHCHANGE: Incomplete
    URLCHANGE: Incomplete

class RootModule(Submodule):
    k_root_name: str
    def __init__(self, repo: Repo) -> None: ...
    def update(
        self,
        previous_commit: Union[Commit_ish, None] = ...,
        recursive: bool = ...,
        force_remove: bool = ...,
        init: bool = ...,
        to_latest_revision: bool = ...,
        progress: Union[None, "RootUpdateProgress"] = ...,
        dry_run: bool = ...,
        force_reset: bool = ...,
        keep_going: bool = ...,
    ) -> RootModule: ...
    def module(self) -> Repo: ...
