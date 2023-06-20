"""
Disko is Fabricius's solution to manage locally installed templates.
"""

import pathlib
import shutil
import typing
from pathlib import Path

from platformdirs import user_data_path

from fabricius.app.config import Config
from fabricius.exceptions import ConflictError
from fabricius.utils import determine_kind

PATH: typing.Final = user_data_path("fabricius", ensure_exists=True) / "downloads"


class DiskoReport(typing.TypedDict):
    name: str
    """
    The name of the project.
    """

    path: Path
    """
    The path of the project.
    """

    kind: typing.Literal["cookiecutter", "fabricius"] | None
    """
    The kind of project, either CookieCutter, or Fabricius.
    None if not known.
    """


def create_report(project: pathlib.Path, as_name: str | None = None) -> DiskoReport:
    kind = determine_kind(project)
    return DiskoReport(name=as_name or project.name, path=project, kind=kind)


def list_available_projects() -> list[DiskoReport]:
    config = Config.get()

    return [create_report(path, as_name=name) for name, path in config.stored_repos.items()]


def save_project(path: pathlib.Path, *, name: str | None = None) -> DiskoReport:
    """
    Attempt to save a project in Disko's path.
    This operation can take time.

    Parameters
    ----------
    path : :py:class:`pathlib.Path`
        The path to the original project that will be saved.
    name : :py:class:`str`
        The name of the project, optional, if omitted, the name of the folder is used.

    Returns
    -------
    DiskoReport
        A report about the saved project.
    """
    config = Config.get()

    name = name or path.name

    if name in config.stored_repos.keys():
        raise ConflictError(config, f"{name} already exist in config.")

    new_folder = shutil.copytree(path, PATH / name)
    path = pathlib.Path(new_folder)

    config.stored_repos[name or path.name] = path
    config.persist()

    return create_report(path, name)
