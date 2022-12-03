from typing import Dict, Optional
from rich import get_console
from rich.console import Console
from rich.style import Style
from rich.text import Text

from fabricius.generator.file import FileGenerator, GeneratorCommitResult
from fabricius.plugins.generator import GeneratorPlugin


class GeneratorRichPlugin(GeneratorPlugin):
    verbose: bool
    """
    Indicate if the plugin should print more information than usual.
    """

    console: Console
    """
    The console used to print results.
    """

    def __init__(self, *, verbose: bool = False) -> None:
        self.verbose = verbose
        self.console = get_console()

    def _print_column(self, title: str, message: str, color: str | None):
        text = Text(f" {title} ", Style(bgcolor=color))
        text.append(f" {message}", Style(bgcolor="black", color=color))
        self.console.print(text)

    def setup(self):
        if self.verbose:
            self.console.print("[green]:white_check_mark: Rich plugin connected to the generator!")

    def teardown(self):
        if self.verbose:
            self.console.print(
                "[yellow]:put_litter_in_its_place: Rich plugin is being disconnected from the generator."
            )

    def on_file_add(self, file: FileGenerator):
        if self.verbose:
            self.console.print(f"[green]:heavy_plus_sign: File added: [underline]{file.name}")

    def before_execution(self):
        if self.verbose:
            self.console.print(
                '[yellow]:stopwatch: ".execute" was called. Generator is about to run!'
            )

    def before_file_commit(self, file: FileGenerator):
        if self.verbose:
            self.console.print(f":mag: {file.name} is about to be committed!")

    def after_file_commit(self, file: FileGenerator):
        self._print_column("COMMITTED", file.name, "green")

    def on_commit_fail(self, file: FileGenerator, exception: Exception):
        self._print_column("FAILURE", f"{file.name} is a failure!", "red")
        self.console.print_exception()

    def after_execution(self, results: Dict[FileGenerator, Optional[GeneratorCommitResult]]):
        return super().after_execution(results)
