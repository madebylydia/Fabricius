import typing
from copy import deepcopy
from pathlib import Path

import yaml


class Config(typing.TypedDict):
    cookiecutters_dir: str
    replay_dir: str
    default_context: dict[typing.Any, typing.Any]
    abbreviations: dict[str, str]


class ParsedConfig(typing.TypedDict):
    cookiecutters_dir: Path
    replay_dir: Path
    default_context: dict[typing.Any, typing.Any]
    abbreviations: dict[str, str]


DEFAULT_CONFIG: Config = {
    "cookiecutters_dir": str(Path("~/.cookiecutters/").expanduser()),
    "replay_dir": str(Path("~/.cookiecutter_replay/").expanduser()),
    "default_context": {},
    "abbreviations": {
        "gh": "https://github.com/{0}.git",
        "gl": "https://gitlab.com/{0}.git",
        "bb": "https://bitbucket.org/{0}",
    },
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


def get_config() -> ParsedConfig:
    conf_data = read_config_file()

    data: Config = deep_merge(DEFAULT_CONFIG, conf_data)  # wtf?

    return ParsedConfig(
        cookiecutters_dir=Path(data["cookiecutters_dir"]).expanduser(),
        replay_dir=Path(data["replay_dir"]).expanduser(),
        default_context=data["default_context"],
        abbreviations=data["abbreviations"],
    )
