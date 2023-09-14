from typing import IO, Dict, List, Sequence, Tuple, Type, Union

from _typeshed import Incomplete
from git.db import GitCmdObjectDB
from git.objects.tree import TreeCacheTup
from git.types import PathLike
from git.util import IndexFileSHA1Writer

from .base import IndexFile
from .typ import BaseIndexEntry, IndexEntry

S_IFGITLINK: Incomplete

def hook_path(name: str, git_dir: PathLike) -> str: ...
def run_commit_hook(name: str, index: IndexFile, *args: str) -> None: ...
def stat_mode_to_index_mode(mode: int) -> int: ...
def write_cache(
    entries: Sequence[Union[BaseIndexEntry, "IndexEntry"]],
    stream: IO[bytes],
    extension_data: Union[None, bytes] = ...,
    ShaStreamCls: Type[IndexFileSHA1Writer] = ...,
) -> None: ...
def entry_key(*entry: Union[BaseIndexEntry, PathLike, int]) -> Tuple[PathLike, int]: ...
def read_cache(
    stream: IO[bytes],
) -> Tuple[int, Dict[Tuple[PathLike, int], "IndexEntry"], bytes, bytes]: ...
def write_tree_from_cache(
    entries: List[IndexEntry], odb: GitCmdObjectDB, sl: slice, si: int = ...
) -> Tuple[bytes, List["TreeCacheTup"]]: ...
