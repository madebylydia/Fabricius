import typing


class WrappedInCookiecutter(typing.TypedDict):
    """A simple typed dict that englob another dict inside a "cookiecutter" key."""

    cookiecutter: dict[str, typing.Literal["_template", "_repo_dir", "_output_dir"] | typing.Any]
