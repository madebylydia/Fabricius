from typing import List, Sequence, Tuple, Union

from _typeshed import Incomplete
from git.compat import safe_decode as safe_decode
from git.repo.base import Repo as Repo
from git.types import PathLike as PathLike
from git.util import remove_password_if_present as remove_password_if_present
from gitdb.exc import BadName as BadName
from gitdb.exc import *

class GitError(Exception): ...
class InvalidGitRepositoryError(GitError): ...
class WorkTreeRepositoryUnsupported(InvalidGitRepositoryError): ...
class NoSuchPathError(GitError, OSError): ...
class UnsafeProtocolError(GitError): ...
class UnsafeOptionError(GitError): ...

class CommandError(GitError):
    command: Incomplete
    status: Incomplete
    stdout: Incomplete
    stderr: Incomplete
    def __init__(
        self,
        command: Union[List[str], Tuple[str, ...], str],
        status: Union[str, int, None, Exception] = ...,
        stderr: Union[bytes, str, None] = ...,
        stdout: Union[bytes, str, None] = ...,
    ) -> None: ...

class GitCommandNotFound(CommandError):
    def __init__(
        self, command: Union[List[str], Tuple[str], str], cause: Union[str, Exception]
    ) -> None: ...

class GitCommandError(CommandError):
    def __init__(
        self,
        command: Union[List[str], Tuple[str, ...], str],
        status: Union[str, int, None, Exception] = ...,
        stderr: Union[bytes, str, None] = ...,
        stdout: Union[bytes, str, None] = ...,
    ) -> None: ...

class CheckoutError(GitError):
    failed_files: Incomplete
    failed_reasons: Incomplete
    valid_files: Incomplete
    def __init__(
        self,
        message: str,
        failed_files: Sequence[PathLike],
        valid_files: Sequence[PathLike],
        failed_reasons: List[str],
    ) -> None: ...

class CacheError(GitError): ...
class UnmergedEntriesError(CacheError): ...

class HookExecutionError(CommandError):
    def __init__(
        self,
        command: Union[List[str], Tuple[str, ...], str],
        status: Union[str, int, None, Exception],
        stderr: Union[bytes, str, None] = ...,
        stdout: Union[bytes, str, None] = ...,
    ) -> None: ...

class RepositoryDirtyError(GitError):
    repo: Incomplete
    message: Incomplete
    def __init__(self, repo: Repo, message: str) -> None: ...
