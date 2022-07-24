import pathlib
import unittest

import fabricius.generator


class TestGenerator(unittest.TestCase):
    """
    Test Fabricius's generator.
    """

    def test_generator_add_file(self):
        """
        Attempt to add a file to the generator.
        """
        generator = fabricius.generator.Generator()
        file = generator.add_file("test", "py")
        self.assertIn(file, generator.files)

    def test_generator_generate_file(self):
        """
        Attempt to generate a file from the generator.
        """
        generator = fabricius.generator.Generator()
        file = generator.add_file("test", "txt")
        expectation = "Hello to the world!"
        path = pathlib.Path("./tests/results/generators")
        file_path = path.joinpath("test.txt")
        file.from_content("Hello to {object}").with_data({"object": "the world!"}).to_directory(
            path, recursive=True
        )

        generator.execute()

        self.assertTrue(file_path.exists())
        self.assertEqual(expectation, file_path.read_text())
