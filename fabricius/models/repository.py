import pathlib

from fabricius.models.template import Template


class Repository:
    path: pathlib.Path
    """
    The root path of the template.
    """

    templates: list[Template]
    """
    A dict containing the list of templates this repository is holding.

    The key represent the name of the template, the value is its path.
    """

    def __init__(self, path: pathlib.Path, templates: list[Template]) -> None:
        self.path = path
        self.templates = templates

    @classmethod
    def new(cls, path: pathlib.Path):
        pass
