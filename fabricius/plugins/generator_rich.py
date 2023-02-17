import typing

from rich import get_console
from rich.console import Console
from rich.prompt import Confirm

from ..file import File, FileCommitResult
from ..plugins.define import GeneratorPlugin


class FileRichPlugin(GeneratorPlugin):
    verbose: bool
    """
    Indicate if the plugin should print more information than usual.
    """

    console: Console
    """
    The console used to print results.
    """

    ask_for_overwrites: bool
    """
    A boolean indicating if the plugin should ask for overwrites when needed.
    """

    PIID = "fabricius.file.rich-221564"

    def __init__(self, *, ask_for_overwrites: bool = True, verbose: bool = False) -> None:
        self.ask_for_overwrites = ask_for_overwrites
        self.verbose = verbose

        self.console = get_console()

    def _print_column(self, title: str, message: str, color: str | None):
        self.console.print(f"[on {color}] {title} [/] [{color}]{message}[/]")

    def setup(self) -> None:
        if self.verbose:
            self.console.print("[green]:white_check_mark: Rich plugin connected to the generator!")

    def teardown(self) -> None:
        if self.verbose:
            self.console.print(
                "[yellow]:put_litter_in_its_place: Rich plugin is being disconnected from the generator."
            )

    def on_file_add(self, file: File) -> None:
        if self.verbose:
            self.console.print(f"[green]:heavy_plus_sign: File added: [underline]{file.name}")

    def before_execution(self) -> None:
        if self.verbose:
            self.console.print(
                '[yellow]:stopwatch: ".execute" was called. Generator is about to run!'
            )

    def before_file_commit(self, file: File) -> None:
        if self.verbose:
            self.console.print(f":mag: {file.name} is about to be committed!")

    def after_file_commit(self, file: File, result: typing.Optional[FileCommitResult]) -> None:
        if self.verbose:
            self.console.print(f":mag: {file.name} was committed!")
        self._print_column("COMMITTED", file.name, "green")

    def on_commit_fail(self, file: File, exception: Exception) -> None:
        match exception:
            case FileExistsError():
                self._print_column("CONFLICT", f"{file.name} already exists", "blue")
                if self.ask_for_overwrites:
                    if Confirm.ask("[blue]Overwrite?"):
                        result = file.commit(overwrite=True)
                        self.generator.results[file] = result
                elif self.verbose:
                    self.console.print(":x: Ignored FileExistsError exception")
            case _:
                self._print_column("FAILURE", f"{file.name} has failed!", "red")
                self.console.print_exception()

    def after_execution(
        self, results: typing.Dict[File, typing.Optional[FileCommitResult]]
    ) -> typing.Any:
        if self.verbose:
            self.console.print("[green]:wave: Execution done!")
