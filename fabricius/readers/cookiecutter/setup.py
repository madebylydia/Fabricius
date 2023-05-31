import json
import pathlib
import sys
import typing
from fnmatch import fnmatch
from functools import partial

from rich import get_console
from rich.prompt import Confirm, Prompt

from fabricius.app.signals import after_template_commit, before_template_commit
from fabricius.app.ui import TemplateProgressBar
from fabricius.exceptions import TemplateError
from fabricius.models.file import File, FileCommitResult
from fabricius.models.renderer import Renderer
from fabricius.models.template import Template
from fabricius.readers.cookiecutter.config import get_config
from fabricius.readers.cookiecutter.exceptions import FailedHookError
from fabricius.readers.cookiecutter.hooks import AvailableHooks, adapt, get_hooks
from fabricius.renderers.jinja_renderer import JinjaRenderer
from fabricius.types import PathStrOrPath
from fabricius.utils import fetch_me_a_beer, sentence_case

EXTENSIONS = [
    "fabricius.readers.cookiecutter.extensions.JsonifyExtension",
    "fabricius.readers.cookiecutter.extensions.RandomStringExtension",
    "fabricius.readers.cookiecutter.extensions.SlugifyExtension",
    "fabricius.readers.cookiecutter.extensions.UUIDExtension",
    "jinja2_time.TimeExtension",
]


Context = typing.NewType("Context", dict[str, typing.Any])
QuestionContext = typing.NewType("QuestionContext", dict[str, typing.Any])
CookieContext = typing.NewType("CookieContext", dict[str, typing.Any])


class CopyRender(Renderer):
    def render(self, content: str) -> str:
        return content


def obtain_template_path(base_folder: pathlib.Path) -> pathlib.Path | None:
    return next(
        (
            path
            for path in base_folder.iterdir()
            if "cookiecutter" in path.name and "{{" in path.name and "}}" in path.name
        ),
        None,
    )


def wrap_in_cookie(data: Context) -> CookieContext:
    return CookieContext({"cookiecutter": data})


def obtain_files(
    base_folder: pathlib.Path, output_folder: pathlib.Path, data: CookieContext
) -> list[File]:
    files: list[File] = []
    for file_path in base_folder.iterdir():
        if file_path.is_file():
            if "{{" in file_path.name and "}}" in file_path.name:
                file_name = JinjaRenderer(data).render(file_path.name)
            else:
                file_name = file_path.name
            file = File(file_name).from_file(file_path).to_directory(output_folder)
            if should_copy_not_render(file, data):
                file.with_renderer(CopyRender)
            else:
                file.use_jinja()
            files.append(file)
    return files


def should_copy_not_render(file: File, context: CookieContext) -> bool:
    if not context["cookiecutter"].get("_copy_without_render"):
        return False
    to_ignore: list[str] = context["cookiecutter"]["_copy_without_render"]
    for index, value in enumerate(to_ignore):
        # Render the string
        to_ignore[index] = JinjaRenderer(context).render(value)
    return any(fnmatch(str(file.compute_destination()), value) for value in to_ignore)


def read_context_raw(file: pathlib.Path) -> Context:
    if not file.exists():
        raise TemplateError(file.parent.name, f"{file.name} does not exist")
    content = file.read_text()

    try:
        context_data = json.loads(content)
    except json.JSONDecodeError as exception:
        raise TemplateError(
            file.parent.name, f"{file.name} does not appear to be a valid JSON file"
        ) from exception

    return Context(context_data)


def get_questions_only(context: Context) -> QuestionContext:
    question_context = {key: value for key, value in context.items() if not key.startswith("_")}
    return QuestionContext(question_context)


def get_answer(prompts: QuestionContext, *, no_prompt: bool = False) -> dict[str, typing.Any]:
    answers: dict[str, typing.Any] = {}

    for question, default_value in prompts.items():
        if isinstance(default_value, list):
            default_value = typing.cast(list[str], default_value)
            prompt = partial(Prompt(sentence_case(question), choices=default_value))
        else:
            prompt = partial(Prompt(sentence_case(question)), default=default_value)
        answer = "" if no_prompt else prompt()
        answers[question] = answer

    return answers


def setup(
    base_folder: PathStrOrPath,
    output_folder: PathStrOrPath,
    *,
    allow_hooks: bool = False,
    extra_context: dict[str, typing.Any] | None = None,
    no_prompt: bool = False,
) -> Template[type[JinjaRenderer]]:
    """Setup a template that will be able to be ran once created.

    Parameters
    ----------
    base_folder : :py:const:`PathStrOrPath <fabricius.types.PathStrOrPath>`
        The folder where the template is located. (Choose the folder where the ``cookiecutter.json``
        is located, not the template itself)
    output_folder : :py:const:`PathStrOrPath <fabricius.types.PathStrOrPath>`
        The folder where the template/files will be created once rendered.
    extra_context : :py:const:`Data <fabricius.types.Data>`, optional
        Any extra context to pass to the template.
        It will override the user's prompt.
    no_prompt : bool, optional
        If set to True, no questions will be asked to the user. By default False

    Returns
    -------
    Type of :py:class:`fabricius.models.template.Template`
        The Template that has been generated.
        It is ready to be committed, and everything has been setup.

    Raises
    ------
    :py:exc:`fabricius.exceptions.TemplateError`
        Exception raised when there's an issue with the template that is most probably due to the
        template's misconception.
    """
    if extra_context is None:
        extra_context = {}

    # Obtain the required information first
    base_folder = pathlib.Path(base_folder).resolve()
    output_folder = pathlib.Path(output_folder).resolve()

    # Prepare contexts
    cookiecutter_config_path = base_folder.joinpath("cookiecutter.json")
    user_config = get_config()

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
    template = Template(output_folder, JinjaRenderer)
    for extension in EXTENSIONS:
        template.renderer.environment.add_extension(extension)
    if context.get("_extensions"):
        for extension in context["_extensions"]:
            template.renderer.environment.add_extension(extension)

    # Add some additional context
    final_context = wrap_in_cookie(context)
    final_context["cookiecutter"] |= {
        "_template": str(template_folder.resolve()),
        "_repo_dir": str(base_folder.resolve()),
        "_output_dir": str(output_folder.resolve()),
    }

    # Begin to get user's prompts.
    questions = get_questions_only(context)
    prompts = get_answer(questions, no_prompt=no_prompt)

    prompts.update(extra_context)

    final_context["cookiecutter"].update(user_config["default_context"])
    final_context["cookiecutter"].update(dict(prompts.items()))
    output_folder = output_folder.joinpath(
        JinjaRenderer(final_context).render(template_folder.name)
    )

    files = obtain_files(template_folder, output_folder, final_context)
    template.add_files(files)
    template.push_data(final_context)

    if allow_hooks:
        connect_hooks(hooks)

    return template


def connect_hooks(hooks: AvailableHooks):
    if hook_path := hooks["pre_gen_project"]:
        before_template_commit.connect(adapt(hook_path, "pre"))  # type: ignore
    if hook_path := hooks["post_gen_project"]:
        after_template_commit.connect(adapt(hook_path, "post"))  # type: ignore


def run(
    template: Template[type[JinjaRenderer]],
    ask_overwrite: bool = True,
    *,
    overwrite: bool = False,
    keep_on_failure: bool = False,
) -> list[FileCommitResult]:
    """Run the CookieCutter template generated using :py:func:`.setup`

    Parameters
    ----------
    template : Type of :py:class:`fabricius.models.template.Template`
        The template to render.
    """
    console = get_console()

    def attempt(force: bool) -> list[FileCommitResult]:
        progress = TemplateProgressBar(len(template.files))
        with progress.begin(fetch_me_a_beer()):
            return template.commit(overwrite=force)

    try:
        return attempt(overwrite)
    except FileExistsError as exception:
        if not ask_overwrite:
            console.print(f"[cyan]{exception.filename}[/] already exist, not overwriting.")
        answer = Confirm.ask(
            f"File [cyan]{exception.filename}[/] already exists, this probably means that this template has already been created. Overwrite?"
        )
        if answer:
            return attempt(True)
    except FailedHookError as exception:
        if exception.exit_code:
            sys.exit(exception.exit_code)
        else:
            get_console().print(exception)
            sys.exit(1)
    except Exception as exception:
        console.print_exception()
        console.print(f"An exception has occurred during committing: {exception}")

        if not keep_on_failure:
            template.cleanup("unlink")
    return []
