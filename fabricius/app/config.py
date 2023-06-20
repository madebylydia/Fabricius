import json
import typing
from pathlib import Path

from platformdirs import user_config_path

DEFAULT_CONFIG: "SerializedConfig" = {"stored_repos": {}}
CONFIG_PATH = user_config_path("fabricius", ensure_exists=True) / "user.json"


def read_config() -> "SerializedConfig":
    if not CONFIG_PATH.exists():
        write_to_config(json.dumps(DEFAULT_CONFIG))

    data = json.loads(CONFIG_PATH.read_text())

    final = DEFAULT_CONFIG.copy()
    final.update(data)
    return final


def write_to_config(content: str) -> None:
    file = CONFIG_PATH
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()
    file.write_text(content)


class SerializedConfig(typing.TypedDict):
    stored_repos: dict[str, str]


class Config:
    stored_repos: dict[str, Path]

    def __init__(self, *, stored_repos: dict[str, Path]) -> None:
        self.stored_repos = stored_repos

    def serialize(self) -> SerializedConfig:
        return SerializedConfig(
            stored_repos={key: str(value.resolve()) for key, value in self.stored_repos.items()}
        )

    def to_json(self) -> str:
        return json.dumps(self.serialize())

    def persist(self) -> None:
        write_to_config(self.to_json())

    @classmethod
    def get(cls) -> "Config":
        data = read_config()

        return cls(stored_repos={key: Path(value) for key, value in data["stored_repos"].items()})
