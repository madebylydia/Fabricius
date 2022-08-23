from fabricius.errors import IntegrityError
from fabricius.template import Template


class IntegrityChecker:
    """
    Check the integrity of a template.
    """

    def check(self, template: Template) -> None:
        if not template.path.joinpath("forge.py").exists():
            raise IntegrityError(template.name, "Missing configuration file (forge.py)")