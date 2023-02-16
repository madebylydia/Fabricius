import unittest

from fabricius.plugin import Plugin, AcceptPlugins


class NeutralPlugin(Plugin):
    pass

class NeutralEmitter(AcceptPlugins[NeutralPlugin]):
    pass


class TestPlugin(unittest.TestCase):
    """
    Test Fabricius's Plugin.
    """
    def test_is_connected(self):

        plugin = NeutralPlugin()
        self.assertFalse(plugin.is_connected)

        emitter = NeutralEmitter()
        emitter.connect_plugin(plugin)
        self.assertTrue(plugin.is_connected)

    def test_piid(self):

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
