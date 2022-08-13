import json
import pathlib
from copy import copy
from os import PathLike
from typing import Dict, Optional, TypedDict, Union

import platformdirs
from git.repo import Repo

from fabricius.errors import FabriciusError, RepoAlreadyExistError

PATH = platformdirs.user_config_path("fabricius", "predeactor").joinpath("config.json")


def create_default_config_file() -> None:
    """
    Create the config file.
    Use this function only if the file does not exist! This will erase the whole actual config.
    """
    defaults = get_config_data_default()
    PATH.parent.mkdir(parents=True)
    PATH.touch()
    PATH.write_text(json.dumps(defaults))


def get_config_data_default() -> "ConfigData":
    return ConfigData(config_version=1, repos={})


class ConfigData(TypedDict):
    """
    A typed dict of the config file.
    """

    config_version: int
    repos: Dict[str, Union[str, PathLike[str]]]


class Config:
    """
    Is it a safe way to interact with the Fabricius's config?
    Yes.

    Should you use it?
    No.

    :meta private:

    Peace!
    """

    data: ConfigData

    def __init__(self, data: ConfigData) -> None:
        self.data = data
        self.__original = data

    def save_repo(self, repo: Repo, alias: Optional[str] = None):
        """
        Add a repo into the config.

        Parameters
        ----------
        repo : :py:class:`git.repo.Repo`
            The repository to add.
        alias : Optional, :py:class:`str`
            An alias for the repository. If omitted, the repo's name will be used.

        Raises
        ------
        :py:exc:`fabricius.errors.FabriciusError` :
            If the repo does not have the :py:attr:`git.repo.Repo.working_tree_dir` property filled.
        :py:exc:`fabricius.errors.RepoAlreadyExistError` :
            If the alias for this repo already exists.
        """
        if not repo.working_tree_dir:
            raise FabriciusError(
                "Repo does not have any working directory associated. Is it cloned?"
            )
        alias = alias or pathlib.Path(repo.working_tree_dir).parts[-1]
        if self.data["repos"].get(alias):
            raise RepoAlreadyExistError(alias)
        self.data["repos"][alias] = repo.working_tree_dir

    def remove_repo(self, alias: str):
        """
        Remove a repo from the config.

        Parameters
        ----------
        alias : :py:class:`str`
            The repository's alias.

        Raises
        ------
        :py:exc:`KeyError` :
            If the repo is not contained in the config.
        """
        del self.data["repos"][alias]

    def save(self):
        """
        Save new values to config file.
        """
        PATH.write_text(json.dumps(self.data))
        self.__original = copy(self.data)

    @property
    def is_dirty(self) -> bool:
        """
        Determine if this instance of Config is dirty.

        Returns
        -------
        :py:class:`bool` :
            If this instance is dirty, aka. not saved locally.
        """
        return self.data == self.__original

    @classmethod
    def get_config(cls):
        """
        Obtain an instance of the Config by reading the Config file stored on this computer.

        Returns
        -------
        :py:class:`~Config` :
            This class.
        """

        if not PATH.exists():
            create_default_config_file()

        config_str = PATH.read_text()
        config_dict = json.loads(config_str)
        return cls(config_dict)
