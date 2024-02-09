import logging
import pathlib
import typing
from fnmatch import fnmatch

from fabricius.composers import JinjaComposer
from fabricius.configurator.reader.cookiecutter import (
    CookieCutterConfigReader,
    CookieCutterExtra,
)
from fabricius.configurator.universal import QuestionConfig, UniversalConfig
from fabricius.exceptions.invalid_template.missing_config import MissingConfigException
from fabricius.exceptions.precondition_exception import PreconditionException
from fabricius.models.file import File
from fabricius.models.generator import Generator
from fabricius.readers.cookiecutter.config import get_config
from fabricius.readers.cookiecutter.hooks import AvailableHooks, get_hooks
from fabricius.readers.cookiecutter.types import WrappedInCookiecutter
from fabricius.utils import determine_file_destination, get_files_only_recursively

_log = logging.getLogger(__name__)
EXTENSIONS = [
    "fabricius.readers.cookiecutter.extensions.JsonifyExtension",
    "fabricius.readers.cookiecutter.extensions.RandomStringExtension",
    "fabricius.readers.cookiecutter.extensions.SlugifyExtension",
    "fabricius.readers.cookiecutter.extensions.UUIDExtension",
    "jinja2_time.TimeExtension",
]


def to_template_path(base_folder: pathlib.Path) -> pathlib.Path | None:
    return next(
        (
            path
            for path in base_folder.iterdir()
            if "cookiecutter" in path.name and "{{" in path.name and "}}" in path.name
        ),
        None,
    )


class FileInfo(typing.TypedDict):
    """A dict containing information about a file."""

    name: str
    source: pathlib.Path
    output: pathlib.Path


class CookieCutterBuilder:
    """Builder for CookieCutter-based templates.

    This will render the template and deposit it in the output folder.
    It facilitates (or at least, should facilitate) the rendering of the template by calling the
    necessary methods only.
    """

    source: pathlib.Path
    """The source folder where the template is located."""

    output: pathlib.Path
    """The output folder where the template will be rendered."""

    extra_context: dict[str, typing.Any]
    """Any extra context to add to the final context."""

    answers: dict[str, typing.Any]
    """The answers to the prompts."""

    delete_on_failure: bool
    """Defines if the output folder should be deleted if the execution fails."""

    config: UniversalConfig[CookieCutterExtra]
    """The context class."""

    def __init__(
        self,
        source_folder: pathlib.Path,
        output_folder: pathlib.Path,
    ) -> None:
        """Create a new CookieCutter builder.

        Parameters
        ----------
        source_folder : pathlib.Path
            The source folder where the template is located.
        output_folder : pathlib.Path
            The output folder where the template will be rendered.

        Raises
        ------
        MissingConfigException
            If the cookiecutter.json file is not found.
        """
        self.source = source_folder.resolve()
        self.output = output_folder.resolve()

        cookiecutter_path = (source_folder / "cookiecutter.json").resolve()
        if not cookiecutter_path.exists():
            raise MissingConfigException(self.source, "cookiecutter.json")
        self.config = CookieCutterConfigReader(cookiecutter_path).obtain()

        self.delete_on_failure = True
        self.answers = {}
        self.extra_context = {}

    def computed_output(self) -> pathlib.Path:
        composer = self.get_composer()
        context = self.get_final_context()
        if self.has_template_path:
            template_path = to_template_path(self.source)
            assert template_path
            return self.output / composer.push_data(context).render(template_path.name)
        return self.output

    @property
    def files(self) -> list[pathlib.Path]:
        """Return all files in the source folder.
        Does not translate their name.
        """
        return get_files_only_recursively(self.get_template_path())

    @property
    def hooks(self) -> AvailableHooks:
        """Return all hooks in the source folder."""
        return get_hooks(self.source)

    def should_copy(self, file: File):
        """Determine if a file should be copied or rendered.

        Parameters
        ----------
        file : :py:class:`File <fabricius.models.file.File>`
            The file we're checking.
        """
        to_ignore: list[str] = self.config.extra["_copy_without_render"]
        context = self.get_final_context()
        for index, value in enumerate(to_ignore):
            to_ignore[index] = JinjaComposer().push_data(context).render(value)
        return any(fnmatch(str(file.compute_destination()), value) for value in to_ignore)

    def render_files_names(self) -> list[FileInfo]:
        """Render files with their rendered name, and their destination path."""
        files: list[FileInfo] = []
        composer = self.get_composer()
        composer.push_data(self.get_final_context())
        for file in self.files:
            destination = determine_file_destination(
                file, self.get_template_path(), self.computed_output()
            )
            files.append(
                FileInfo(
                    name=composer.render(file.name),
                    source=file.resolve(),
                    output=destination.resolve(),
                )
            )
        return files

    @property
    def has_template_path(self) -> bool:
        return bool(to_template_path(self.source))

    def get_template_path(self) -> pathlib.Path:
        """Return the path to the template.

        Exceptions
        ----------
        :py:exc:`fabricius.exceptions.PreconditionException` :
            If the template path is not found.
        """
        if path := to_template_path(self.source):
            return path
        raise PreconditionException(self, "Template path not found")

    def get_questions(self) -> list[QuestionConfig]:
        """Return the questions to ask to the user."""
        return self.config.questions

    def get_composer(self) -> JinjaComposer:
        composer = JinjaComposer()
        for extension in (*EXTENSIONS, *self.config.extra["_extensions"]):
            composer.environment.add_extension(extension)
        return composer

    def get_generator(self) -> Generator[JinjaComposer]:
        return Generator(self.get_composer())

    def get_final_context(self) -> WrappedInCookiecutter:
        """Obtain the final context for this template and the data that have been passed.
        This will wrap the data into a "cookiecutter" key, and add metadata information about this
        template. (_template, _repo_dir, _output_dir)
        """
        data: dict[str, typing.Any] = {}

        user_config = get_config()

        data |= user_config["default_context"]
        data |= self.extra_context
        data |= self.answers

        data |= {
            "_template": str(self.get_template_path().resolve()),
            "_repo_dir": str(self.source.resolve()),
            "_output_dir": str(self.output.resolve()),
        }

        return {"cookiecutter": data}

    def execute(self, overwrite: bool = False):
        """Execute this builder.

        This will render the files, and deposit them in the destination folder.

        Parameters
        ----------
        overwrite : bool
            If the files should be overwritten if they already exist.
        """
        generator = self.get_generator()
        for file_info in self.render_files_names():
            file = File(file_info["name"])
            file.from_content(file_info["source"].read_text()).to_directory(
                file_info["output"]
            ).with_composer(self.get_composer())
            generator.add_file(file)

        # That has been troublesome to try to implement "correctly", if you have a better
        # suggestion here, feel free to throw a PR.
        # Makes me unhappy, but I can't throw that directly in "get_final_context" because
        # that would make an infinite loop with "computed_output".
        fixed_data = self.get_final_context()
        fixed_data["cookiecutter"]["_output_dir"] = str(self.computed_output().resolve())

        generator.with_data(self.get_final_context())
        generator.overwrite(overwrite)
        generator.atomic(self.delete_on_failure)
        generator.to_directory(self.output)
        generator.execute()
