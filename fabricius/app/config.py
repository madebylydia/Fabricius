import json
from pathlib import Path
from typing import TypedDict

from platformdirs import user_config_path

DEFAULT_CONFIG: "SerializedConfig" = {"stored_repos": {}}
CONFIG_FILE = "user.json"


def read_config() -> "SerializedConfig":
    config_file = user_config_path("fabricius").joinpath(CONFIG_FILE)
    if not config_file.exists():
        write_to_config(json.dumps(DEFAULT_CONFIG))

    data: "SerializedConfig" = json.loads(config_file.read_text())

    final = DEFAULT_CONFIG.copy()
    final.update(data)
    return final


def write_to_config(content: str) -> None:
    file = user_config_path("fabricius").joinpath(CONFIG_FILE)
    if not file.exists():
        file.parent.mkdir(parents=True)
        file.touch()
    file.write_text(content)


class SerializedConfig(TypedDict):
    stored_repos: dict[str, str]


class Config:
    stored_repos: dict[str, Path]

    def __init__(self, *, stored_repos: dict[str, Path]) -> None:
        self.stored_repos = stored_repos

    def serialize(self) -> SerializedConfig:
        return SerializedConfig(
            stored_repos={key: str(value.resolve()) for key, value in self.stored_repos.items()}
        )

    @classmethod
    def get(cls) -> "Config":
        data = read_config()

        return cls(stored_repos={key: Path(value) for key, value in data["stored_repos"].items()})
