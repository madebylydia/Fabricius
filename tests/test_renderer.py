import pytest

from fabricius.models.renderer import Renderer
from fabricius.renderers import (
    ChevronRenderer,
    PythonFormatRenderer,
    StringTemplateRenderer,
)


@pytest.fixture
def dumb_renderer() -> "type[Renderer]":
    class MyRenderer(Renderer):
        def render(self, content: str) -> str:
            return content.format(self.data)

    return MyRenderer


def test_renderer_data(dumb_renderer: type[Renderer]):
    """
    Test Renderer's data availability.
    """
    assert isinstance(dumb_renderer({}).data, dict)


def test_python_format_renderer():
    """
    Test Python Format renderer.
    """
    renderer = PythonFormatRenderer({"name": "Python Format"})
    result = renderer.render("I am {name}")

    assert result == "I am Python Format"


def test_string_template_renderer():
    """
    Test String Template renderer.
    """
    renderer = StringTemplateRenderer({"name": "String Template"})
    result = renderer.render("I am $name")
    assert result == "I am String Template"

    renderer = StringTemplateRenderer({"name_renderer": "String Template"}, safe=False)
    with pytest.raises(KeyError):
        renderer.render("I am $name")


def test_chevron_renderer():
    """
    Test Chevron (Mustache) renderer.
    """
    renderer = ChevronRenderer(
        {
            "name": "Chevron",
            "value": 10000,
            "taxed_value": 10000 - (10000 * 0.4),
            "in_ca": True,
        }
    )
    result = renderer.render(
        "Hello {{name}}\nYou have just won {{value}} dollars!\n{{#in_ca}}\nWell, {{taxed_value}} dollars, "
        "after taxes.{{/in_ca}}"
    )

    assert (
        result
        == "Hello Chevron\nYou have just won 10000 dollars!\nWell, 6000.0 dollars, after taxes."
    )
