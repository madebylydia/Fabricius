from typing import NamedTuple, Sequence, Tuple, Union

from _typeshed import Incomplete
from git.objects import Blob
from git.repo import Repo
from git.types import PathLike

StageType = int

class BlobFilter:
    paths: Incomplete
    def __init__(self, paths: Sequence[PathLike]) -> None: ...
    def __call__(self, stage_blob: Tuple[StageType, Blob]) -> bool: ...

class BaseIndexEntryHelper(NamedTuple):
    mode: int
    binsha: bytes
    flags: int
    path: PathLike
    ctime_bytes: bytes
    mtime_bytes: bytes
    dev: int
    inode: int
    uid: int
    gid: int
    size: int

class BaseIndexEntry(BaseIndexEntryHelper):
    def __new__(
        cls,
        inp_tuple: Union[
            Tuple[int, bytes, int, PathLike],
            Tuple[int, bytes, int, PathLike, bytes, bytes, int, int, int, int, int],
        ],
    ) -> BaseIndexEntry: ...
    @property
    def hexsha(self) -> str: ...
    @property
    def stage(self) -> int: ...
    @classmethod
    def from_blob(cls, blob: Blob, stage: int = ...) -> BaseIndexEntry: ...
    def to_blob(self, repo: Repo) -> Blob: ...

class IndexEntry(BaseIndexEntry):
    @property
    def ctime(self) -> Tuple[int, int]: ...
    @property
    def mtime(self) -> Tuple[int, int]: ...
    @classmethod
    def from_base(cls, base: BaseIndexEntry) -> IndexEntry: ...
    @classmethod
    def from_blob(cls, blob: Blob, stage: int = ...) -> IndexEntry: ...
