from typing import AnyStr, overload

from _typeshed import Incomplete
from gitdb.utils.encoding import force_bytes as force_bytes
from gitdb.utils.encoding import force_text as force_text

is_win: bool
is_posix: Incomplete
is_darwin: Incomplete
defenc: Incomplete

@overload
def safe_decode(s: None) -> None: ...
@overload
def safe_decode(s: AnyStr) -> str: ...
@overload
def safe_encode(s: None) -> None: ...
@overload
def safe_encode(s: AnyStr) -> bytes: ...
@overload
def win_encode(s: None) -> None: ...
@overload
def win_encode(s: AnyStr) -> bytes: ...
