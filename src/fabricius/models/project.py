import pathlib
import typing

PROJECT_STATE: typing.TypeAlias = typing.Literal["pending", "processing", "failed", "persisted"]


class Project:
    """
    Class that represent a project that will be rendered from a
    :py:class:`fabricius.models.library.Library`.
    """

    destination: pathlib.Path

    state: PROJECT_STATE

    _will_fake: bool
