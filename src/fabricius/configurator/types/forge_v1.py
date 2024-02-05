import pathlib
import typing


class QuestionV1[QuestionType: typing.Any](typing.TypedDict, total=False):
    """Fabricius-centric typed dict for questions to ask to the users."""

    id: typing.Required[str]
    help: str
    prompt: str
    type: QuestionType
    default: QuestionType
    choices: list[str]


class TemplateV1(typing.TypedDict):
    """Fabricius-centric typed dict for configuration of templates."""

    version: typing.Literal[1]
    type: typing.Literal["template"]
    root: pathlib.Path
    method: typing.Literal["run", "setup"]
    questions: list[QuestionV1[typing.Any]]


class RepositoryV1(typing.TypedDict):
    """Fabricius-centric typed dict for configuration of a repository."""

    version: typing.Literal[1]
    type: typing.Literal["repository"]
    root: pathlib.Path
    templates: dict[str, pathlib.Path]
