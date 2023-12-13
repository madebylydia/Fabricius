import pathlib
import typing

import yaml

from fabricius.utils import deep_merge


class Config(typing.TypedDict):
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
    conf_data = read_config_file(file or pathlib.Path("~/.cookiecutterrc").expanduser())
    data = deep_merge(DEFAULT_CONFIG, conf_data)
    return Config(default_context=data["default_context"])
