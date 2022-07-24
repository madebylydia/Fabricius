import pathlib
import shutil
import unittest

from fabricius.file import FileGenerator


class TestFile(unittest.TestCase):
    """
    Test Fabricius's file.
    """

    BASE_PATH: str = "./tests/templates/file/{}"
    DESTINATION: str = "./tests/results/file"

    def test_render_with_python_format(self):
        """
        Attempt to render a file with Python format.
        """
        file = FileGenerator("result_python_format", "txt")
        file.from_file(self.BASE_PATH.format("python_template.txt")).to_directory(
            self.DESTINATION
        ).with_data({"name": "Python Formatting"})
        file.commit()

    def test_render_with_mustache(self):
        """
        Attempt to render a file with Chevron (Mustache formatting) format.
        """
        file = FileGenerator("result_mustache_template", "txt")
        file.from_file(self.BASE_PATH.format("mustache_template.mustache")).to_directory(
            self.DESTINATION
        ).with_data({"name": "Chevron"}).use_mustache()
        file.commit()

    def test_render_with_string_template(self):
        """
        Attempt to render a file with String.template format.
        """
        file = FileGenerator("result_string_template", "txt")
        file.from_file(self.BASE_PATH.format("string_template.txt")).to_directory(
            self.DESTINATION
        ).with_data({"name": "String Template"}).use_string_template()
        file.commit()

    def test_create_recursive(self):
        """
        Attempt to create a file recursively.
        """
        path = pathlib.Path(f"{self.DESTINATION}/with/some/recursive/folder")

        def clean_folder():
            """
            Cleanup function before running tests.
            """
            if path.exists():
                shutil.rmtree(pathlib.Path(f"{self.DESTINATION}/with"))

        clean_folder()

        file = FileGenerator("recursive_file", "txt")
        file.from_file(self.BASE_PATH.format("python_template.txt")).with_data(
            {"name": "Python Formatting with a bit of recursive folders!"}
        )

        with self.assertRaises((FileNotFoundError, NotADirectoryError)):
            file.to_directory(path, recursive=False)

        file.to_directory(path, recursive=True)
        result = file.commit()
        self.assertIs(result["state"], "persisted")
        self.assertTrue(path.exists())
