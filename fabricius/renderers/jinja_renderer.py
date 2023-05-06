from jinja2 import BaseLoader, Environment

from fabricius.models.renderer import Renderer


class JinjaRenderer(Renderer):
    name = "Jinja Template"

    environment: Environment = Environment(loader=BaseLoader())

    def render(self, content: str) -> str:
        return self.environment.from_string(content).render(**self.data)
