import os
import pathlib
from typing import List, Optional

from fabricius.template import Template


def get_templates_path(*, at: Optional[pathlib.Path] = None) -> pathlib.Path:
    return pathlib.Path(at or os.getcwd(), "templates")


def templates_path_is_valid(*, at: Optional[pathlib.Path] = None) -> bool:
    path_to_templates = get_templates_path(at=at)
    return bool(path_to_templates.exists() and path_to_templates.is_dir())


def available_internal_templates(*, at: Optional[pathlib.Path] = None) -> List[Template]:
    """
    Return a list of available templates.
    """
    return (
        [
            Template(name=path.name, path=path, type="internal")
            for path in get_templates_path(at=at).iterdir()
        ]
        if templates_path_is_valid(at=at)
        else []
    )


def get_template(template_name: str) -> Optional[pathlib.Path]:
    if template_name in [t.name for t in available_internal_templates()]:
        return get_templates_path().joinpath(template_name)
