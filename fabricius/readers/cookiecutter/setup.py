import json
import pathlib
import sys
import typing
from functools import partial

from rich import get_console
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.prompt import Prompt, PromptBase
from rich.text import TextType

from fabricius.app.signals import after_template_commit, before_template_commit
from fabricius.exceptions import TemplateError
from fabricius.models.file import File
from fabricius.models.template import Template
from fabricius.readers.cookiecutter.exceptions import FailedHookError
from fabricius.readers.cookiecutter.hooks import adapt, get_hooks
from fabricius.renderers.jinja_renderer import JinjaRenderer
from fabricius.types import Data, PathStrOrPath
from fabricius.utils import fetch_me_a_beer, sentence_case

EXTENSIONS = [
    "fabricius.readers.cookiecutter.extensions.JsonifyExtension",
    "fabricius.readers.cookiecutter.extensions.RandomStringExtension",
    "fabricius.readers.cookiecutter.extensions.SlugifyExtension",
    "fabricius.readers.cookiecutter.extensions.UUIDExtension",
    "jinja2_time.TimeExtension",
]


class ChoicesPrompt(PromptBase[typing.Any]):
    available_choices: int | None

    def __init__(
        self,
        prompt: TextType = "",
        *,
        console: Console | None = None,
        password: bool = False,
        choices: list[str] | None = None,
        show_default: bool = True,
        show_choices: bool = True,
    ) -> None:
        super().__init__(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )


def obtain_template_path(base_folder: pathlib.Path) -> pathlib.Path | None:
    return next(
        (
            path
            for path in base_folder.iterdir()
            if "cookiecutter" in path.name and "{{" in path.name and "}}" in path.name
        ),
        None,
    )


def obtain_files(base_folder: pathlib.Path, output_folder: pathlib.Path, data: Data) -> list[File]:
    files: list[File] = []
    for file_path in base_folder.iterdir():
        if file_path.is_file():
            if "{{" in file_path.name and "}}" in file_path.name:
                file_name = JinjaRenderer(data).render(file_path.name)
            else:
                file_name = file_path.name
            file = File(file_name).from_file(file_path).use_jinja().to_directory(output_folder)
            files.append(file)
    return files


def read_context_raw(file: pathlib.Path) -> dict[str, typing.Any]:
    if not file.exists():
        raise TemplateError(file.parent.name, f"{file.name} does not exist")
    content = file.read_text()

    try:
        context_data: dict[str, typing.Any] = json.loads(content)
    except json.JSONDecodeError as exception:
        raise TemplateError(
            file.parent.name, f"{file.name} does not appear to be a valid JSON file"
        ) from exception

    return context_data


def get_questions_only(context: dict[str, typing.Any]):
    context = {key: value for key, value in context.items() if not key.startswith("_")}
    return context


def get_answer(prompts: dict[str, typing.Any]) -> dict[str, typing.Any]:
    answers: dict[str, typing.Any] = {}

    for question, default_value in prompts.items():
        if isinstance(default_value, list):
            default_value = typing.cast(list[str], default_value)
            prompt = partial(ChoicesPrompt(sentence_case(question), choices=default_value))
        else:
            prompt = partial(Prompt(sentence_case(question)), default=default_value)
        answer = prompt()
        if answer is None:
            answer = ""
        answers[question] = answer

    return answers


def setup(
    base_folder: PathStrOrPath,
    output_folder: PathStrOrPath,
    *,
    extra_context: dict[str, typing.Any] = {},
    no_prompt: bool = False,
) -> Template[type[JinjaRenderer]]:
    # Obtain the required information first
    base_folder = pathlib.Path(base_folder).resolve()
    output_folder = pathlib.Path(output_folder).resolve()

    # Prepare contexts
    cookiecutter_config_path = base_folder.joinpath("cookiecutter.json")
    final_context: dict[str, typing.Any] = {"cookiecutter": {}}

    # Ensure a cookiecutter.json file exists.
    # Obtains the context's raw content & the template's hooks.
    if not cookiecutter_config_path.exists():
        raise TemplateError(base_folder.name, "cookiecutter.json does not exist")
    context = read_context_raw(cookiecutter_config_path)
    hooks = get_hooks(base_folder)

    # Obtain the location of the template, if any.
    template_folder = obtain_template_path(base_folder)
    if not template_folder:
        raise TemplateError(base_folder.name, "No template found")

    # Get the template object
    template = Template(template_folder, JinjaRenderer)
    for extension in EXTENSIONS:
        template.renderer.environment.add_extension(extension)
    if context.get("_extensions"):
        for extension in context["_extensions"]:
            template.renderer.environment.add_extension(extension)

    # Add some additional context
    final_context["cookiecutter"] |= {
        "_template": str(template_folder.resolve()),
        "_repo_dir": str(base_folder.resolve()),
        "_output_dir": str(output_folder.resolve()),
    }

    # Begin to get user's prompts.
    questions = get_questions_only(context)
    prompts = get_answer(questions)

    final_context["cookiecutter"].update(dict(prompts.items()))

    files = obtain_files(template_folder, output_folder, final_context)
    template.add_files(files)
    template.push_data(final_context)

    if hooks:
        if hook_path := hooks["pre_gen_project"]:
            before_template_commit.connect(adapt(hook_path, "pre"))  # type: ignore
        if hook_path := hooks["post_gen_project"]:
            after_template_commit.connect(adapt(hook_path, "post"))  # type: ignore

    return template


def run(template: Template[type[JinjaRenderer]]):
    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress:
            progress.add_task(fetch_me_a_beer(), start=False)
            template.commit()
    except FailedHookError as exception:
        if exception.exit_code:
            sys.exit(exception.exit_code)
        else:
            get_console().print(exception)
            sys.exit(1)
