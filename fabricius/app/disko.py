"""
Disko is Fabricius's solution to manage locally installed templates.
"""

import typing
from pathlib import Path

from platformdirs import user_data_path

from fabricius.exceptions import FabriciusError
from fabricius.forge_reader import read_forge_file

PATH = user_data_path("fabricius").joinpath("downloads")
if not PATH.exists():
    PATH.mkdir(parents=True)


class DiskoReport(typing.TypedDict):
    name: str
    path: Path

    kind: typing.Literal["cookiecutter", "fabricius"]


def list_available_projects() -> list[DiskoReport]:
    reports: list[DiskoReport] = []

    for path in PATH.iterdir():
        if not path.is_dir():
            raise FabriciusError(f"ILLEGAL CONFLICT: Orphan file detected: {path.resolve()}.")

        forge_file = path.joinpath("forge.py")

        if not forge_file.exists():
            reports.append(
                DiskoReport(name=path.name, path=path, is_repository=None, kind="fabricius")
            )
        data = read_forge_file(path)
        reports.append(
            DiskoReport(
                name=path.name,
                path=path,
                is_repository=data["type"] == "repository",
                appears_valid_forge=True,
            )
        )

    return reports
