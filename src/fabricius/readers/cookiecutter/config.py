import pathlib
import typing

import yaml

from fabricius.utils import deep_merge


class Config(typing.TypedDict):
    """The configuration for cookiecutter. *sigh*, not much use but it is what it is..."""

    default_context: dict[typing.Any, typing.Any]


DEFAULT_CONFIG: Config = {
    "default_context": {},
}


def read_config_file(file: pathlib.Path) -> Config:
    try:
        config = file.read_text()
        return yaml.safe_load(config)
    except FileNotFoundError:
        return DEFAULT_CONFIG


def get_config(file: pathlib.Path | None = None) -> Config:
    """Obtain the config content from the user's cookiecutter's configuration file."""
    conf_data = read_config_file(file or pathlib.Path("~/.cookiecutterrc").expanduser())
    data = deep_merge(dict(DEFAULT_CONFIG), dict(conf_data))
    return Config(default_context=data["default_context"])
