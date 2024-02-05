# pylint: disable=W0223

# Taken from https://github.com/cookiecutter/cookiecutter/blob/0fb68d913116d940a15c407535c88c0d5ab3e7ba/cookiecutter/extensions.py
# Licensed under the BSD 3-Clause License.

import datetime
import json
import string
import typing
import uuid
from secrets import choice

import arrow
from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.parser import Parser
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


class TimeExtension(Extension):
    """Jinja2 Extension for dates and times."""

    tags = {"now"}

    def __init__(self, environment: Environment):
        """Jinja2 Extension constructor."""
        super().__init__(environment)

        environment.extend(datetime_format="%Y-%m-%d")

    def _datetime(
        self, timezone: datetime.timezone, operator: str, offset: str, datetime_format: str | None
    ):
        d = arrow.now(timezone)

        # parse shift params from offset and include operator
        shift_params = {}
        for param in offset.split(","):
            interval, value = param.split("=")
            shift_params[interval.strip()] = float(operator + value.strip())
        d = d.shift(**shift_params)

        if datetime_format is None:
            datetime_format = self.environment.datetime_format  # type: ignore
        assert isinstance(datetime_format, str)
        return d.strftime(datetime_format)

    def _now(self, timezone: datetime.timezone, datetime_format: str | None):
        if datetime_format is None:
            datetime_format = self.environment.datetime_format  # type: ignore
        assert isinstance(datetime_format, str)
        return arrow.now(timezone).strftime(datetime_format)

    def parse(self, parser: "Parser"):
        """Parse datetime template and add datetime value."""
        lineno = next(parser.stream).lineno

        node = parser.parse_expression()

        if parser.stream.skip_if("comma"):
            datetime_format = parser.parse_expression()
        else:
            datetime_format = nodes.Const(None)

        if isinstance(node, nodes.Add):
            call_method = self.call_method(
                "_datetime",
                [node.left, nodes.Const("+"), node.right, datetime_format],
                lineno=lineno,
            )
        elif isinstance(node, nodes.Sub):
            call_method = self.call_method(
                "_datetime",
                [node.left, nodes.Const("-"), node.right, datetime_format],
                lineno=lineno,
            )
        else:
            call_method = self.call_method(
                "_now",
                [node, datetime_format],
                lineno=lineno,
            )
        return nodes.Output([call_method], lineno=lineno)
