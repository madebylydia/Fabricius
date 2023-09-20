import json
import logging
import pathlib
import typing

import platformdirs
import pydantic

from fabricius.exceptions import ExpectationFailedException
from fabricius.utils import deep_merge

_log = logging.getLogger(__name__)
DEFAULT_CONFIG_PATH = platformdirs.user_config_path("fabricius", ensure_exists=True).joinpath(
    "config.json"
)


_F = typing.ParamSpec("_F")
_R = typing.TypeVar("_R")


class Config(pydantic.BaseModel):
    config_file: pathlib.Path | None = pydantic.Field(exclude=True)

    download_path: pathlib.Path

    stored_repositories: dict[str, pathlib.Path]

    @classmethod
    def defaults(cls):
        return cls(
            config_file=None,
            download_path=platformdirs.user_data_path("fabricius").joinpath("downloads"),
            stored_repositories={},
        )

    def persist(self):
        if not self.config_file:
            raise ExpectationFailedException("No config file opened.")
        self.config_file.write_text(self.model_dump_json())

    @classmethod
    def get(cls, file: pathlib.Path | None = None) -> "Config":
        config_file = file or DEFAULT_CONFIG_PATH
        default = True if config_file == DEFAULT_CONFIG_PATH else False

        if not config_file.exists() and default:
            _log.debug(f"Creating new config file at {config_file.resolve()}")
            config_file.parent.touch()
            config_file.touch()
            config_file.write_text(Config.defaults().model_dump_json())

        defaults_as_dict = Config.defaults().model_dump()

        data = config_file.read_text()
        data_as_dict = json.loads(data)

        final = deep_merge(defaults_as_dict, data_as_dict)
        final["config_file"] = config_file

        return cls(**final)
