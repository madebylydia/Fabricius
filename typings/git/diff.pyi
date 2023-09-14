from typing import Any, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from _typeshed import Incomplete
from git.repo.base import Repo
from git.types import PathLike

from .objects import Commit
from .objects.tree import Tree

NULL_TREE: Incomplete

class Diffable:
    class Index: ...
    repo: Incomplete
    def diff(
        self,
        other: Union[Type["Index"], "Tree", "Commit", None, str, object] = ...,
        paths: Union[PathLike, List[PathLike], Tuple[PathLike, ...], None] = ...,
        create_patch: bool = ...,
        **kwargs: Any
    ) -> DiffIndex: ...

T_Diff = TypeVar("T_Diff", bound="Diff")

class DiffIndex(List[T_Diff]):
    change_type: Incomplete
    def iter_change_type(self, change_type: Lit_change_type) -> Iterator[T_Diff]: ...

class Diff:
    re_header: Incomplete
    NULL_HEX_SHA: Incomplete
    NULL_BIN_SHA: Incomplete
    a_rawpath: Incomplete
    b_rawpath: Incomplete
    a_mode: Incomplete
    b_mode: Incomplete
    a_blob: Incomplete
    b_blob: Incomplete
    new_file: Incomplete
    deleted_file: Incomplete
    copied_file: Incomplete
    raw_rename_from: Incomplete
    raw_rename_to: Incomplete
    diff: Incomplete
    change_type: Incomplete
    score: Incomplete
    def __init__(
        self,
        repo: Repo,
        a_rawpath: Optional[bytes],
        b_rawpath: Optional[bytes],
        a_blob_id: Union[str, bytes, None],
        b_blob_id: Union[str, bytes, None],
        a_mode: Union[bytes, str, None],
        b_mode: Union[bytes, str, None],
        new_file: bool,
        deleted_file: bool,
        copied_file: bool,
        raw_rename_from: Optional[bytes],
        raw_rename_to: Optional[bytes],
        diff: Union[str, bytes, None],
        change_type: Optional[Lit_change_type],
        score: Optional[int],
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    @property
    def a_path(self) -> Optional[str]: ...
    @property
    def b_path(self) -> Optional[str]: ...
    @property
    def rename_from(self) -> Optional[str]: ...
    @property
    def rename_to(self) -> Optional[str]: ...
    @property
    def renamed(self) -> bool: ...
    @property
    def renamed_file(self) -> bool: ...
