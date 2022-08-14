import json
import pathlib
from copy import copy
from os import PathLike
from typing import Dict, List, Optional, TypedDict, Union

import git
import platformdirs

from fabricius.errors import RepoAlreadyExistError

CONFIG_PATH = platformdirs.user_config_path("fabricius").joinpath("config.json")


def create_default_config_file() -> None:
    """
    Create the config file.
    Use this function only if the file does not exist! This will erase the whole actual config.

    :meta private:
    """
    defaults = get_config_data_default()
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True)
    CONFIG_PATH.touch()
    CONFIG_PATH.write_text(json.dumps(defaults))


def get_config_data_default() -> "ConfigData":
    return ConfigData(config_version=1, repos={})


class ConfigData(TypedDict):
    """
    A typed dict of the config file.
    """

    config_version: int
    """
    The version of the config.
    """

    repos: Dict[str, Union[str, PathLike[str]]]
    """
    A dict with the alias of the template and it's path.
    """


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

    def save_repo(self, repo: Union[str, PathLike[str], git.Repo], alias: Optional[str] = None):
        """
        Add a repo into the config.

        Parameters
        ----------
        template : :py:class:`fabricius.Template`
            The template to add.
        alias : Optional, :py:class:`str`
            An alias for the template. If omitted, the repo's name will be used.

        Raises
        ------
        :py:exc:`fabricius.errors.FabriciusError` :
            If the repo does not have the :py:attr:`git.repo.Repo.working_tree_dir` property filled.
        :py:exc:`fabricius.errors.RepoAlreadyExistError` :
            If the alias for this repo already exists.
        """
        path: pathlib.Path

        if isinstance(repo, git.Repo):
            path = pathlib.Path(repo.working_tree_dir)
        else:
            path = pathlib.Path(repo)
        print(path)

        if alias:
            # Replace the parent path by it's alias
            path = path.parent.joinpath(alias)

        if path.exists():
            raise RepoAlreadyExistError(str(path))

        self.data["repos"][alias or str(path.parent)] = str(path.resolve())

    def remove_repo(self, alias: str) -> None:
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

    def list_repos(self) -> List[git.Repo]:
        """
        Return a list of repositories.

        Returns
        -------
        List of :py:class:`git.Repo` :
            The list of available repositories.
        """
        return [git.Repo(path) for path in self.data["repos"].values()]

    def get_repo(self, alias: str) -> git.Repo:
        """
        Return a repository, if it exists.

        Parameters
        ----------
        alias : :py:class:`str`
            The repository's alias.

        Raises
        ------
        :py:exc:`KeyError` :
            If the repository does not exist.

        Returns
        -------
        :py:class:`git.Repo` :
            The repository.
        """
        repo_path = self.data["repos"][alias]
        return git.Repo(repo_path)

    def save(self) -> None:
        """
        Save new values to config file.
        """
        CONFIG_PATH.write_text(json.dumps(self.data))
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
    def get_config(cls, *, create_if_no_exist: bool = True):
        """
        Obtain an instance of the Config by reading the Config file stored on this computer.

        Parameters
        ----------
        create_if_no_exist : :py:class:`bool`
            Create the ``config.json`` file if it does not exist. Default to True.

        Raises
        ------
        :py:exc:`FileNotFoundError` :
            If ``config.json`` does not exist and that ``create_if_no_exist`` is on ``False``.

        Returns
        -------
        :py:class:`~Config` :
            This class.
        """

        if not CONFIG_PATH.exists():
            if not create_if_no_exist:
                raise FileNotFoundError("'config.json' does not exist.")
            create_default_config_file()

        config_str = CONFIG_PATH.read_text()
        config_dict = json.loads(config_str)
        return cls(config_dict)
