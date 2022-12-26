import enum
import pathlib
import unittest
from typing import Dict, Optional, Type

from typing_extensions import Self

from fabricius.errors import FabriciusError
from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.generator.generator import Generator
from fabricius.plugins.generator import GeneratorPlugin


class Signals(enum.Enum):
    SETUP = "SETUP"
    TEARDOWN = "TEARDOWN"
    ON_FILE_ADD = "ON_FILE_ADD"
    BEFORE_EXECUTION = "BEFORE_EXECUTION"
    BEFORE_FILE_COMMIT = "BEFORE_FILE_COMMIT"
    AFTER_FILE_COMMIT = "AFTER_FILE_COMMIT"
    AFTER_EXECUTION = "AFTER_EXECUTION"
    ON_COMMIT_FAIL = "ON_COMMIT_FAIL"


class MyPlugin(GeneratorPlugin):
    """
    A simple plugin that show signals when called.
    """

    def __init__(self) -> None:
        self.signals = {
            "SETUP": False,
            "TEARDOWN": False,
            "ON_FILE_ADD": False,
            "BEFORE_EXECUTION": False,
            "BEFORE_FILE_COMMIT": False,
            "AFTER_FILE_COMMIT": False,
            "AFTER_EXECUTION": False,
            "ON_COMMIT_FAIL": False,
        }
        self.raise_setup_error = False

    def setup(self):
        self.signals["SETUP"] = True
        if self.raise_setup_error:
            self.raise_setup_error = False
            raise FabriciusError("Unknown exception!")
        return Signals.SETUP

    def teardown(self):
        self.signals["TEARDOWN"] = True
        return Signals.TEARDOWN

    def on_file_add(self, file: FileGenerator):
        self.signals["ON_FILE_ADD"] = True
        return Signals.ON_FILE_ADD

    def before_execution(self):
        self.signals["BEFORE_EXECUTION"] = True
        return Signals.BEFORE_EXECUTION

    def before_file_commit(self, file: FileGenerator):
        self.signals["BEFORE_FILE_COMMIT"] = True
        return Signals.BEFORE_FILE_COMMIT

    def after_file_commit(self, file: FileGenerator, result: Optional[GeneratorCommitResult]):
        self.signals["AFTER_FILE_COMMIT"] = True
        return Signals.AFTER_FILE_COMMIT

    def after_execution(self, results: Dict[FileGenerator, Optional[GeneratorCommitResult]]):
        self.signals["AFTER_EXECUTION"] = True
        return Signals.AFTER_EXECUTION

    def on_commit_fail(self, file: FileGenerator, exception: Exception):
        self.signals["ON_COMMIT_FAIL"] = True
        return Signals.ON_COMMIT_FAIL

    @classmethod
    def new(cls: Type[Self]) -> Self:
        return cls()


PluginToConnect = MyPlugin()


class TestGenerator(unittest.TestCase):
    """
    Test Fabricius's generator.
    """

    def test_files(self):
        """
        Test Generator's proper files state.
        """
        generator = Generator()
        generator.add_file("test", "txt")
        self.assertIsInstance(generator.files[0], FileGenerator)

    def test_plugin_signals(self):
        """
        Test Generator's plugin "signals".
        """
        generator = Generator()

        def signal_is(signal: Signals, value: bool, *, on: MyPlugin = PluginToConnect):
            signal_name = signal.value
            if value:
                self.assertTrue(on.signals[signal_name])
            else:
                self.assertFalse(on.signals[signal_name])

        generator.connect_plugin(PluginToConnect)
        signal_is(Signals.SETUP, True)
        file = generator.add_file("signals", "txt")
        signal_is(Signals.ON_FILE_ADD, True)
        file.from_content("File created for test_plugin_signals.").to_directory(
            pathlib.Path(__file__, "..", "results", "generator")
        ).with_data({"name": "world"})

        generator.execute()
        signal_is(Signals.BEFORE_EXECUTION, True)
        signal_is(Signals.BEFORE_FILE_COMMIT, True)
        signal_is(Signals.AFTER_FILE_COMMIT, True)
        signal_is(Signals.AFTER_EXECUTION, True)
        signal_is(Signals.ON_COMMIT_FAIL, False)
        generator.disconnect_plugin(PluginToConnect)
        signal_is(Signals.TEARDOWN, True)

        failing_generator = Generator()
        new_plugin = PluginToConnect.new()
        failing_generator.connect_plugin(new_plugin)
        file = generator.add_file("test", "txt")
        with self.assertRaises(Exception):
            generator.execute()
            # Missing required properties for the added file
            signal_is(Signals.ON_COMMIT_FAIL, True, on=new_plugin)
