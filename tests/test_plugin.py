import unittest

from fabricius.interfaces import BasePlugin


class TestBasePlugin(unittest.TestCase):
    """
    Test Fabricius's BasePlugin.
    """

    def test_piid(self):

        class NeutralPlugin(BasePlugin):
            pass

        self.assertFalse(NeutralPlugin().has_valid_piid)
        self.assertIsNone(NeutralPlugin().plugin_name)
        self.assertIsNone(NeutralPlugin().plugin_id)

        class TooShortIDPlugin(BasePlugin):
            PIID = "abc-12345"

        self.assertFalse(TooShortIDPlugin().has_valid_piid)

        class TooShortNamePlugin(BasePlugin):
            PIID = "ob-123456"

        self.assertFalse(TooShortNamePlugin().has_valid_piid)

        class ValidPlugin(BasePlugin):
            PIID = "myplugin-123456"

        self.assertTrue(ValidPlugin().has_valid_piid)
        self.assertEqual(ValidPlugin().plugin_name, "myplugin")
        self.assertEqual(ValidPlugin().plugin_id, 123456)
