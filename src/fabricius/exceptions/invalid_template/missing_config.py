import pathlib

from fabricius.exceptions.invalid_template.base import InvalidTemplateException


class MissingConfigException(InvalidTemplateException):
    """Raised when a template is missing a config file."""

    def __init__(self, base_path: pathlib.Path, expected_file: str):
        super().__init__(
            f'Template at {base_path.resolve()} is missing a config file: Expected "{expected_file}" to '
            "be there."
        )
