import typing


class UnknownQuestionV1(typing.TypedDict, total=False):
    id: typing.Any
    help: typing.Any
    type: typing.Any
    choices: typing.Any


class UnknownForgeV1(typing.TypedDict, total=False):
    """
    A TypedDict of a forge file that is under version 1.

    Only keys are known, their types are unknown, this is up to the validator to check what the
    values are.
    """

    version: typing.Any
    type: typing.Any
    root: typing.Any
    templates: typing.Any
    questions: typing.Any
    plugins: typing.Any
    method: typing.Any
