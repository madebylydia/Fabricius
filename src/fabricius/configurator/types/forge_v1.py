import pathlib
import typing


class QuestionV1(typing.TypedDict):
    id: str
    help: str
    type: typing.Any
    choices: list[str]


class TemplateV1(typing.TypedDict):
    version: typing.Literal[1]
    type: typing.Literal["template"]
    root: pathlib.Path
    method: typing.Literal["run", "setup"]
    questions: list[QuestionV1]


class RepositoryV1(typing.TypedDict):
    version: typing.Literal[1]
    type: typing.Literal["repository"]
    root: pathlib.Path
    templates: dict[str, pathlib.Path]
