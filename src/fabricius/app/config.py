import json
import logging
import pathlib

import platformdirs
import pydantic

from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.utils import deep_merge

_log = logging.getLogger(__name__)
_DEFAULT_CONFIG_PATH = platformdirs.user_config_path("fabricius", ensure_exists=True).joinpath(
    "config.json"
)


def get_or_create_default_config():
    if _DEFAULT_CONFIG_PATH.exists():
        return _DEFAULT_CONFIG_PATH
    _log.info("Creating new config file at %s", _DEFAULT_CONFIG_PATH.resolve())
    _DEFAULT_CONFIG_PATH.touch()
    _DEFAULT_CONFIG_PATH.write_text(Config.defaults().model_dump_json(), encoding="utf-8")
    return _DEFAULT_CONFIG_PATH


class Config(pydantic.BaseModel):
    """The configuration class for Fabricius. This is used in order to know informations such as
    where to store downloaded content, what content is stored, etc.
    """

    config_file: pathlib.Path | None = pydantic.Field(exclude=True)
    """The config file that is used to store the config. Not stored."""

    download_path: pathlib.Path = pydantic.Field()
    """The path where the downloaded repositories will be stored."""

    stored_repositories: dict[str, pathlib.Path] = pydantic.Field()
    """List of stored repositories.
    The key is the alias and the value is the informations about the repository.
    """

    @classmethod
    def defaults(cls) -> "Config":
        """Instantiate a new instance of the class with default values.

        Returns
        -------
        Config
            The newly created instance.
        """
        return cls(
            config_file=None,
            download_path=platformdirs.user_data_path("fabricius").joinpath("downloads"),
            stored_repositories={},
        )

    def persist(self) -> None:
        """Persists the current configuration to a file.
        It requires a config file to be opened. (Done by using the :py:meth:`.load` method)

        Raises
        ------
        :py:exc:`fabricius.exceptions.PreconditionException`
            If no config file is opened, this exception is raised.
        """
        if not self.config_file:
            raise PreconditionException(self, "No config file opened.")
        with self.config_file as file:
            _log.debug("Persisting config at %s", file)
            file.write_text(self.model_dump_json())

    @classmethod
    def load(cls, config_file: pathlib.Path) -> "Config":
        """Load a configuration from the given file.

        Parameters
        ----------
        config_file : pathlib.Path
            The path to the configuration file.

        Returns
        -------
        Config
            A Config object initialized with the loaded configuration.

        """

        data = config_file.read_text()
        data_as_dict = json.loads(data)
        _log.debug("Raw config data (From %s) : %s", config_file.resolve(), data_as_dict)

        final = deep_merge(Config.defaults().model_dump(), data_as_dict)
        final["config_file"] = config_file

        return cls(**final)
