import json
import pathlib
import typing

from fabricius.composers import JinjaComposer
from fabricius.exceptions.expectation_failed_exception import ExpectationFailedException
from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.models.file import File
from fabricius.models.generator import Generator
from fabricius.readers.cookiecutter.builder_config import CookieCutterBuilderConfig
from fabricius.readers.cookiecutter.config import get_config
from fabricius.readers.cookiecutter.types import WrappedInCookiecutter

EXTENSIONS = [
    "fabricius.readers.cookiecutter.extensions.JsonifyExtension",
    "fabricius.readers.cookiecutter.extensions.RandomStringExtension",
    "fabricius.readers.cookiecutter.extensions.SlugifyExtension",
    "fabricius.readers.cookiecutter.extensions.UUIDExtension",
    "jinja2_time.TimeExtension",
]


def obtain_template_path(base_folder: pathlib.Path) -> pathlib.Path | None:
    return next(
        (
            path
            for path in base_folder.iterdir()
            if "cookiecutter" in path.name and "{{" in path.name and "}}" in path.name
        ),
        None,
    )


class CookieCutterBuilder:
    source: pathlib.Path
    """
    The source folder where the template is located.
    """

    output: pathlib.Path
    """
    The output folder where the template will be rendered.
    """

    extra_context: dict[str, typing.Any]
    """
    Any extra context to add to the final context.
    """

    answers: dict[str, typing.Any]
    """
    The answers to the prompts.
    """

    context: CookieCutterBuilderConfig
    """
    The context class.
    """

    def __init__(
        self,
        source_folder: pathlib.Path,
        output_folder: pathlib.Path,
    ) -> None:
        self.source = source_folder
        self.output = output_folder

        cookiecutter_path = (source_folder / "cookiecutter.json").resolve()
        if not cookiecutter_path.exists():
            raise PreconditionException(
                self.source.name, "cookiecutter.json must exist in source folder"
            )
        self.context = CookieCutterBuilderConfig(json.loads(cookiecutter_path.read_text()))

        self.answers = {}
        self.extra_context = {}

    def set_extra_context(self, extra_context: dict[str, typing.Any]) -> typing.Self:
        self.extra_context = extra_context
        return self

    @property
    def files(self) -> list[pathlib.Path]:
        """
        Return all files in the source folder.
        Does not translate their name.
        """
        return [file for file in self.source.iterdir() if file.is_file()]

    def render_files(self) -> dict[str, str]:
        """
        Render all files in the source folder.
        """
        files: dict[str, str] = {}
        composer = self.get_composer()
        composer.push_data(self.get_final_context())
        for file in self.files:
            files[
                str(pathlib.Path(file).parent.resolve().relative_to(self.source).resolve())
            ] = composer.render(file.name)
        return files

    @property
    def has_template_path(self) -> bool:
        return bool(obtain_template_path(self.source))

    def get_template_path(self) -> pathlib.Path:
        """
        Return the template path.
        """
        if path := obtain_template_path(self.source):
            return path
        raise ExpectationFailedException("Template path not found")

    def get_prompts_or_ask(self) -> dict[str, typing.Any]:
        """
        Return the prompts or ask the user for them.
        """
        prompts = self.context.get_prompts()
        if not prompts:
            return {}
        return prompts

    def get_composer(self) -> JinjaComposer:
        composer = JinjaComposer()
        for extension in [*EXTENSIONS, *self.context.get_extensions()]:
            composer.environment.add_extension(extension)
        return composer

    def get_generator(self) -> Generator[JinjaComposer]:
        generator = Generator(self.get_composer())
        return generator

    def get_final_context(self) -> WrappedInCookiecutter:
        data: dict[str, typing.Any] = {}

        user_config = get_config()

        data |= user_config["default_context"]
        data |= self.context.get_default_context()

        data |= {
            "_template": str(self.get_template_path().resolve()),
            "_repo_dir": str(self.source.resolve()),
            "_output_dir": str(self.output.resolve()),
        }

        return {"cookiecutter": data}

    def execute(self):
        generator = self.get_generator()
        for file_destination, file_name in self.render_files().items():
            file = File(file_name)
            file.to_directory(file_destination)
            generator.add_file(file)
        _log
