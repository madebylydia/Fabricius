import pathlib
import unittest

from fabricius.generator.errors import AlreadyCommittedError
from fabricius.generator.file import FileGenerator
from fabricius.generator.renderer import (
    ChevronRenderer,
    PythonFormatRenderer,
    StringTemplateRenderer,
)


class TestFileGenerator(unittest.TestCase):
    """
    Test Fabricius's FileGenerator.
    """

    TEMPLATE_PATH = pathlib.Path(__file__, "..", "files", "templates").resolve()
    DESTINATION_PATH = pathlib.Path(__file__, "..", "results", "file_generator").resolve()

    def test_file_name(self):
        """
        Test FileGenerator's proper name.
        """
        file = FileGenerator("my_file_name")
        self.assertEqual(file.name, "my_file_name")
        file = FileGenerator("my_file_name", "txt")
        self.assertEqual(file.name, "my_file_name.txt")

    def test_file_state(self):
        """
        Test FileGenerator's proper state.
        """
        file = FileGenerator("test")
        self.assertEqual(file.state, "pending")

    def test_file_content(self):
        """
        Test FileGenerator's proper content usage.
        """
        file = FileGenerator("test", "txt")
        file_content = self.TEMPLATE_PATH.joinpath("python_template.txt").read_text()

        with self.assertRaises(FileNotFoundError):
            file.from_file(self.TEMPLATE_PATH.joinpath("idonotexist.txt"))

        file.from_file(self.TEMPLATE_PATH.joinpath("python_template.txt"))
        self.assertEqual(file_content, file.content)

        file.from_content("Hello! I am {name} with some content")
        self.assertEqual("Hello! I am {name} with some content", file.content)

    def test_file_destination(self):
        """
        Test FileGenerator's proper destination.
        """
        file = FileGenerator("test", "txt")

        file.to_directory(self.DESTINATION_PATH)
        self.assertEqual(str(self.DESTINATION_PATH), str(file.destination))

        with self.assertRaises(NotADirectoryError):
            file.to_directory(__file__)

    def test_file_renderer(self):
        """
        Test FileGenerator's proper renderer.
        """
        file = FileGenerator("test", "txt")
        self.assertIs(file.renderer, PythonFormatRenderer)

        file.use_mustache()
        self.assertIs(file.renderer, ChevronRenderer)

        file.use_string_template()
        self.assertIs(file.renderer, StringTemplateRenderer)

        file.with_renderer(PythonFormatRenderer)
        self.assertIs(file.renderer, PythonFormatRenderer)

    def test_file_data(self):
        """
        Test FileGenerator's proper data.
        """
        file = FileGenerator("test", "txt")

        file.with_data({"some": "data"})
        self.assertDictEqual(file.data, {"some": "data"})

        file.with_data({"new": "data"})
        self.assertDictEqual(file.data, {"new": "data"})

        file.with_data({"more": "new data"}, overwrite=False)
        self.assertDictEqual(file.data, {"new": "data", "more": "new data"})

    def test_file_generate(self):
        """
        Test FileGenerator's proper generation.
        """
        file = FileGenerator("test", "txt")

        file.from_content("My name is {name}!")
        file.with_data({"name": "Python"})
        result = file.generate()

        self.assertEqual(result, "My name is Python!")

    def test_file_commit(self):
        """
        Test FileGenerator's proper commit.
        """
        file = FileGenerator("python_result", "txt")

        file.from_file(self.TEMPLATE_PATH.joinpath("python_template.txt")).to_directory(
            self.DESTINATION_PATH
        ).with_data({"name": "Python's format"})

        result = file.commit(overwrite=True)
        self.assertIsInstance(result, dict)
        self.assertTrue(self.DESTINATION_PATH.joinpath("python_result.txt").exists())
        self.assertEqual(file.state, "persisted")

        with self.assertRaises(AlreadyCommittedError):
            file.commit()

        with self.assertRaises(FileExistsError):
            file = FileGenerator("python_result", "txt")
            file.from_file(self.TEMPLATE_PATH.joinpath("python_template.txt")).to_directory(
                self.DESTINATION_PATH
            ).with_data({"name": "Python's format"})
            file.commit()
