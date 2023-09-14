import struct
from typing import Callable

from _typeshed import Incomplete
from git.types import _T, PathLike

pack = struct.pack
unpack = struct.unpack

class TemporaryFileSwap:
    file_path: Incomplete
    tmp_file_path: Incomplete
    def __init__(self, file_path: PathLike) -> None: ...
    def __del__(self) -> None: ...

def post_clear_cache(func: Callable[..., _T]) -> Callable[..., _T]: ...
def default_index(func: Callable[..., _T]) -> Callable[..., _T]: ...
def git_working_dir(func: Callable[..., _T]) -> Callable[..., _T]: ...
