import unittest

from fabricius.renderer import (
    ChevronRenderer,
    PythonFormatRenderer,
    Renderer,
    StringTemplateRenderer,
)


class TestRenderers(unittest.TestCase):
    """
    Test Fabricius's renderers.
    """

    def get_my_renderer(self):
        class MyRenderer(Renderer):
            def render(self, content: str) -> str:
                return content.format(self.data)

        return MyRenderer

    def test_renderer_data(self):
        """
        Test Renderer's data availability.
        """
        renderer = self.get_my_renderer()
        self.assertIsInstance(renderer({}).data, dict)

    def test_python_format_renderer(self):
        """
        Test Python Format renderer.
        """
        renderer = PythonFormatRenderer({"name": "Python Format"})
        result = renderer.render("I am {name}")

        self.assertEqual(result, "I am Python Format")

    def test_string_template_renderer(self):
        """
        Test String Template renderer.
        """
        renderer = StringTemplateRenderer({"name": "String Template"})
        result = renderer.render("I am $name")
        self.assertEqual(result, "I am String Template")

        renderer = StringTemplateRenderer({"name_renderer": "String Template"}, safe=False)
        with self.assertRaises(KeyError):
            renderer.render("I am $name")

    def test_chevron_renderer(self):
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

        self.assertEqual(
            result,
            "Hello Chevron\nYou have just won 10000 dollars!\nWell, 6000.0 dollars, after taxes.",
        )
