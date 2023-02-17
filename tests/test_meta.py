import re
import unittest

from fabricius import __version__ as fabricius_version
from fabricius.interfaces import Singleton
from fabricius.utils import calculate_text_color


class TestProjectMeta(unittest.TestCase):
    def test_version_is_semantic(self):
        # I hope the guy who made this regex rests in peace.
        regex = re.match(
            r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
            fabricius_version,
        )
        self.assertIsNotNone(regex, "Your version is not semantic.")


class TestProjectUtils(unittest.TestCase):
    def test_singleton(self):
        class MySingleton(Singleton):
            pass

        self.assertEqual(id(MySingleton()), id(MySingleton()))

    def test_color_calculation(self):
        self.assertEqual(calculate_text_color("black"), "bright_white")
        self.assertEqual(calculate_text_color("bright_white"), "black")
