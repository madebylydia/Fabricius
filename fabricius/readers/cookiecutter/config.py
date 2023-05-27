import typing
from copy import deepcopy
from pathlib import Path

import yaml


class Config(typing.TypedDict):
    default_context: dict[typing.Any, typing.Any]


DEFAULT_CONFIG: Config = {
    "default_context": {},
}


def read_config_file() -> Config:
    try:
        config = Path("~/.cookiecutterrc").expanduser().read_text()
        return yaml.safe_load(config)
    except FileNotFoundError:
        return DEFAULT_CONFIG


def deep_merge(
    base: dict[typing.Any, typing.Any], update_with: dict[typing.Any, typing.Any]
) -> dict[typing.Any, typing.Any]:
    data = deepcopy(base)

    for key, value in update_with.items():
        if isinstance(value, dict):
            data[key] = deep_merge(base.get(key, {}), value)
        else:
            data[key] = value

    return data


def get_config() -> Config:
    conf_data = read_config_file()

    data: Config = deep_merge(DEFAULT_CONFIG, conf_data)  # wtf?

    return Config(default_context=data["default_context"])
