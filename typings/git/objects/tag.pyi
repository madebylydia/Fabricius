from typing import Union

from _typeshed import Incomplete
from git.repo import Repo
from git.types import Literal
from git.util import Actor

from . import base

class TagObject(base.Object):
    type: Literal["tag"]
    object: Incomplete
    tag: Incomplete
    tagger: Incomplete
    tagged_date: Incomplete
    tagger_tz_offset: Incomplete
    message: Incomplete
    def __init__(
        self,
        repo: Repo,
        binsha: bytes,
        object: Union[None, base.Object] = ...,
        tag: Union[None, str] = ...,
        tagger: Union[None, "Actor"] = ...,
        tagged_date: Union[int, None] = ...,
        tagger_tz_offset: Union[int, None] = ...,
        message: Union[str, None] = ...,
    ) -> None: ...
