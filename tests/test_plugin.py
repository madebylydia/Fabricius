import unittest

from fabricius.plugin import Plugin


class TestPlugin(unittest.TestCase):
    """
    Test Fabricius's Plugin.
    """

    def test_piid(self):

        class NeutralPlugin(Plugin):
            pass

        self.assertFalse(NeutralPlugin().has_valid_piid)
        self.assertIsNone(NeutralPlugin().plugin_name)
        self.assertIsNone(NeutralPlugin().plugin_id)

        class TooShortIDPlugin(Plugin):
            PIID = "abc-12345"

        self.assertFalse(TooShortIDPlugin().has_valid_piid)

        class TooShortNamePlugin(Plugin):
            PIID = "ob-123456"

        self.assertFalse(TooShortNamePlugin().has_valid_piid)

        class ValidPlugin(Plugin):
            PIID = "myplugin-123456"

        self.assertTrue(ValidPlugin().has_valid_piid)
        self.assertEqual(ValidPlugin().plugin_name, "myplugin")
        self.assertEqual(ValidPlugin().plugin_id, 123456)
