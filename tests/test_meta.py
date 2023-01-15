import re
import unittest

import fabricius
from fabricius.interfaces import Singleton


class TestProjectMeta(unittest.TestCase):
    def test_version_is_semantic(self):
        # I hope the guy who made this regex rests in peace.
        regex = re.match(
            r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
            fabricius.__version__,
        )
        self.assertIsNotNone(regex, "Your version is not semantic.")


class TestProjectUtils(unittest.TestCase):
    def test_singleton(self):

        class MySingleton(Singleton):
            pass

        self.assertEqual(id(MySingleton()), id(MySingleton()))
