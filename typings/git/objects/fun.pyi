from typing import Callable, List, Sequence, Tuple, Union

from _typeshed import ReadableBuffer
from git import GitCmdObjectDB

EntryTup = Tuple[bytes, int, str]
EntryTupOrNone = Union[EntryTup, None]

def tree_to_stream(
    entries: Sequence[EntryTup], write: Callable[[ReadableBuffer], Union[int, None]]
) -> None: ...
def tree_entries_from_data(data: bytes) -> List[EntryTup]: ...
def traverse_trees_recursive(
    odb: GitCmdObjectDB, tree_shas: Sequence[Union[bytes, None]], path_prefix: str
) -> List[Tuple[EntryTupOrNone, ...]]: ...
def traverse_tree_recursive(
    odb: GitCmdObjectDB, tree_sha: bytes, path_prefix: str
) -> List[EntryTup]: ...
