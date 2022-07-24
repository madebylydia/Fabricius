import pathlib
from typing import Optional, Type

from typing_extensions import Self

from fabricius.const import Data
from fabricius.contracts import GeneratorFileContract, RendererContract
from fabricius.contracts.file_generator import CommitResult, GeneratorFileExport
from fabricius.errors import NoContentError, NoDestinationError
from fabricius.renderer import (
    ChevronRenderer,
    PythonFormatRenderer,
    StringTemplateRenderer,
)


class FileGenerator(GeneratorFileContract):
    def __init__(self, name: str, extension: Optional[str] = None):
        self.name = f"{name}.{extension}" if extension else name
        self.state = "pending"
        self.content = None
        self.destination = None

        self.renderer = PythonFormatRenderer
        self.data = {}

    def from_file(self, path: str | pathlib.Path) -> Self:
        path = pathlib.Path(path) if isinstance(path, str) else path
        with open(path.absolute(), "r") as file_content:
            self.content = file_content.read()
        return self

    def from_content(self, content: str) -> Self:
        self.content = content
        return self

    def to_directory(self, directory: str | pathlib.Path, *, recursive: bool = True) -> Self:
        path = pathlib.Path(directory).absolute()
        if not path.exists():
            path.mkdir(parents=recursive)
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")
        self.destination = path
        return self

    def use_mustache(self) -> Self:
        self.renderer = ChevronRenderer
        return self

    def use_string_template(self) -> Self:
        self.renderer = StringTemplateRenderer
        return self

    def with_renderer(self, renderer: Type[RendererContract]) -> Self:
        self.renderer = renderer
        return self

    def with_data(self, data: Data, *, overwrite: bool = False) -> Self:
        if overwrite:
            self.data = {}
        self.data.update(data)
        return self

    def generate(self) -> str:
        if not self.content:
            raise NoContentError(self.name)

        return self.renderer(self.data).render(self.content)

    def commit(self, *, overwrite: bool = False) -> CommitResult:
        # Sourcery propose to replace the try-except for contextlib.suppress
        # It is skipped because the state would always be persisted that way, which is wrong.
        # sourcery skip: use-contextlib-suppress
        if not self.destination:
            raise NoDestinationError(self.name)

        final_content = self.generate()
        destination = self.destination.joinpath(self.name)

        if destination.exists() and not overwrite:
            return self._build_commit_result(final_content)

        try:
            destination.write_text(final_content)
            self.state = "persisted"
        except NotADirectoryError:
            pass

        return self._build_commit_result(final_content)

    def to_dict(self) -> GeneratorFileExport:
        return GeneratorFileExport(
            name=self.name,
            state=self.state,
            template_content=self.content,
            destination=self.destination,
            renderer=self.renderer,
            data=self.data,
        )

    def _build_commit_result(self, final_content: str) -> CommitResult:
        """
        Build a commit result.

        It is not recommended to use it in your own codebase.

        Returns
        -------
        CommitResult :
            The commit's result.
        """
        if not self.content:
            raise NoContentError(self.name)
        if not self.destination:
            raise NoDestinationError(self.name)

        return CommitResult(
            state=self.state,
            with_data=self.data,
            template_content=self.content,
            content=final_content,
            path=self.destination.joinpath(self.name),
        )
