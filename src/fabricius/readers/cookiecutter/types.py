import typing


class WrappedInCookiecutter(typing.TypedDict):
    cookiecutter: dict[str, typing.Literal["_template", "_repo_dir", "_output_dir"] | typing.Any]
