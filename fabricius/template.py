import os
import pathlib
from typing import Union, Type
from typing_extensions import Self

from fabricius.contracts.template import TemplateContract, TemplateDict, TemplateType
from fabricius.errors import TemplateNotFound
from fabricius.internal_utils import get_external_templates_path


class Template(TemplateContract):
    def __init__(self, name: str, path: pathlib.Path, type: TemplateType) -> None:
        self.name = name
        self.path = path
        self.type = type

    def to_dict(self):
        return TemplateDict(
            name=self.name,
            path=self.path,
            type=self.type,
        )

    @classmethod
    def from_cwd(cls: Type[Self], template_name_or_path: Union[str, pathlib.Path]):
        path = pathlib.Path(os.getcwd(), "templates", template_name_or_path)
        if not path.exists() or not path.is_dir():
            print(path)
            raise TemplateNotFound(
                template_name_or_path.name
                if isinstance(template_name_or_path, pathlib.Path)
                else template_name_or_path
            )
        # All templates in the cwd are internal
        # (Unless you're fucking cwd is the damn external templates folder...)
        return cls(
            path.name, path, "internal"
        )

    @classmethod
    def from_external_template(cls: Type[Self], template_name: str):
        base_path = get_external_templates_path()
        path = base_path.joinpath(template_name)
        if not path.exists() or not path.is_dir():
            raise TemplateNotFound(template_name)
        return cls(
            path.name, path, "external"
        )
