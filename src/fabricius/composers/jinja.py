from jinja2 import BaseLoader, Environment

from fabricius.models.composer import Composer


class JinjaComposer(Composer):
    name = "Jinja Template"

    environment: Environment = Environment(loader=BaseLoader())
    """
    The environment the composer will use.
    It is suggested for developers to directly interact with this attribute.
    The loader is the default jinja2's BaseLoader.
    """

    def render(self, content: str) -> str:
        return self.environment.from_string(content).render(self.data)
