import abc
from abc import abstractmethod
from datetime import datetime, timedelta, tzinfo
from subprocess import Popen
from typing import (
    Any,
    Callable,
    Iterator,
    NamedTuple,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from _typeshed import Incomplete
from git.types import Literal, Protocol
from git.util import Actor as Actor
from git.util import IterableList, IterableObj

from .blob import Blob
from .commit import Commit
from .tag import TagObject
from .tree import Tree

class TraverseNT(NamedTuple):
    depth: int
    item: Union["Traversable", "Blob"]
    src: Union["Traversable", None]

T_TIobj = TypeVar("T_TIobj", bound="TraversableIterableObj")

def get_object_type_by_name(
    object_type_name: bytes,
) -> Union[Type["Commit"], Type["TagObject"], Type["Tree"], Type["Blob"]]: ...
def utctz_to_altz(utctz: str) -> int: ...
def altz_to_utctz_str(altz: int) -> str: ...
def verify_utctz(offset: str) -> str: ...

class tzoffset(tzinfo):
    def __init__(self, secs_west_of_utc: float, name: Union[None, str] = ...) -> None: ...
    def __reduce__(self) -> Tuple[Type["tzoffset"], Tuple[float, str]]: ...
    def utcoffset(self, dt: Union[datetime, None]) -> timedelta: ...
    def tzname(self, dt: Union[datetime, None]) -> str: ...
    def dst(self, dt: Union[datetime, None]) -> timedelta: ...

utc: Incomplete

def parse_date(string_date: Union[str, datetime]) -> Tuple[int, int]: ...
def parse_actor_and_date(line: str) -> Tuple[Actor, int, int]: ...

class ProcessStreamAdapter:
    def __init__(self, process: Popen, stream_name: str) -> None: ...
    def __getattr__(self, attr: str) -> Any: ...

class Traversable(Protocol):
    @abstractmethod
    def list_traverse(self, *args: Any, **kwargs: Any) -> Any: ...
    @abstractmethod
    def traverse(self, *args: Any, **kwargs: Any) -> Any: ...

class Serializable(Protocol): ...

class TraversableIterableObj(IterableObj, Traversable, metaclass=abc.ABCMeta):
    TIobj_tuple = Tuple[Union[T_TIobj, None], T_TIobj]
    def list_traverse(self, *args: Any, **kwargs: Any) -> IterableList[T_TIobj]: ...
    @overload
    def traverse(self) -> Iterator[T_TIobj]: ...
    @overload
    def traverse(
        self,
        predicate: Callable[[Union[T_TIobj, Tuple[Union[T_TIobj, None], T_TIobj]], int], bool],
        prune: Callable[[Union[T_TIobj, Tuple[Union[T_TIobj, None], T_TIobj]], int], bool],
        depth: int,
        branch_first: bool,
        visit_once: bool,
        ignore_self: Literal[True],
        as_edge: Literal[False],
    ) -> Iterator[T_TIobj]: ...
    @overload
    def traverse(
        self,
        predicate: Callable[[Union[T_TIobj, Tuple[Union[T_TIobj, None], T_TIobj]], int], bool],
        prune: Callable[[Union[T_TIobj, Tuple[Union[T_TIobj, None], T_TIobj]], int], bool],
        depth: int,
        branch_first: bool,
        visit_once: bool,
        ignore_self: Literal[False],
        as_edge: Literal[True],
    ) -> Iterator[Tuple[Union[T_TIobj, None], T_TIobj]]: ...
    @overload
    def traverse(
        self,
        predicate: Callable[[Union[T_TIobj, TIobj_tuple], int], bool],
        prune: Callable[[Union[T_TIobj, TIobj_tuple], int], bool],
        depth: int,
        branch_first: bool,
        visit_once: bool,
        ignore_self: Literal[True],
        as_edge: Literal[True],
    ) -> Iterator[Tuple[T_TIobj, T_TIobj]]: ...
