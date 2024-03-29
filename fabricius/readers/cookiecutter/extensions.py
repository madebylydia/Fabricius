# Taken from https://github.com/cookiecutter/cookiecutter/blob/cf81d63bf3d82e1739db73bcbed6f1012890e33e/cookiecutter/extensions.py

import json
import string
import typing
import uuid
from secrets import choice

from jinja2 import Environment
from jinja2.ext import Extension
from slugify import slugify as pyslugify  # type: ignore


class JsonifyExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def jsonify(obj: object) -> str:
            return json.dumps(obj, sort_keys=True, indent=4)

        environment.filters["jsonify"] = jsonify  # type: ignore


class RandomStringExtension(Extension):
    """Jinja2 extension to create a random string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension Constructor."""
        super().__init__(environment)

        def random_ascii_string(length: int, punctuation: bool = False) -> str:
            if punctuation:
                corpus = "".join((string.ascii_letters, string.punctuation))
            else:
                corpus = string.ascii_letters
            return "".join(choice(corpus) for _ in range(length))

        environment.globals.update(random_ascii_string=random_ascii_string)  # type: ignore


class SlugifyExtension(Extension):
    """Jinja2 Extension to slugify string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        def slugify(value: typing.Any, **kwargs: typing.Any) -> str:
            """Slugifies the value."""
            return pyslugify(value, **kwargs)

        environment.filters["slugify"] = slugify  # type: ignore


class UUIDExtension(Extension):
    """Jinja2 Extension to generate uuid4 string."""

    def __init__(self, environment: Environment) -> None:
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        def uuid4() -> str:
            """Generate UUID4."""
            return str(uuid.uuid4())

        environment.globals.update(uuid4=uuid4)  # type: ignore
