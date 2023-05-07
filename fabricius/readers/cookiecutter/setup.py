import json
import pathlib
import typing

from fabricius.exceptions import TemplateError
from fabricius.models.file import File
from fabricius.models.question import Question
from fabricius.models.template import Template
from fabricius.renderers.jinja_renderer import JinjaRenderer
from fabricius.types import Data, PathStrOrPath
from fabricius.utils import sentence_case

EXTENSIONS = [
    "fabricius.readers.cookiecutter.extensions.JsonifyExtension",
    "fabricius.readers.cookiecutter.extensions.RandomStringExtension",
    "fabricius.readers.cookiecutter.extensions.SlugifyExtension",
    "fabricius.readers.cookiecutter.extensions.UUIDExtension",
]


def obtain_template_path(base_folder: pathlib.Path) -> pathlib.Path:
    for path in base_folder.iterdir():
        if "cookiecutter" in path.name and "{{" in path.name and "}}" in path.name:
            return path
    raise TemplateError(base_folder.name, "No template found")


def obtain_files(base_folder: pathlib.Path, output_folder: pathlib.Path, data: Data) -> list[File]:
    files: list[File] = []
    for file_path in base_folder.iterdir():
        if file_path.is_file():
            if "{{" in file_path.name and "}}" in file_path.name:
                file_name = JinjaRenderer(data).render(file_path.name)
            else:
                file_name = file_path.name
            file = File(file_name)
            file.from_file(file_path)
            file.use_jinja()
            file.to_directory(output_folder)
            files.append(file)
    return files


def read_questions(file: pathlib.Path) -> list[Question[typing.Any]]:
    if not file.exists():
        raise TemplateError(file.parent.name, f"{file.name} does not exist")
    content = file.read_text("utf-8")

    try:
        questions_data: dict[str, typing.Any] = json.loads(content)
    except json.JSONDecodeError as exception:
        raise TemplateError(
            file.parent.name, f"{file.name} does not appear to be a valid JSON file"
        ) from exception

    questions: list[Question[typing.Any]] = []
    for name, value in questions_data.items():
        if value == "":
            value = None
        question: Question[typing.Any] = Question(name, help=sentence_case(name), default=value)
        questions.append(question)

    return questions


def obtain_user_input(questions: list[Question[typing.Any]]) -> None:
    for question in questions:
        if question.question_id.startswith("__"):
            continue
        question.get_answer()


def setup(folder: PathStrOrPath, output_folder: PathStrOrPath) -> Template[type[JinjaRenderer]]:
    folder = pathlib.Path(folder).resolve()
    output_folder = pathlib.Path(output_folder).resolve()

    if not folder.joinpath("cookiecutter.json"):
        raise TemplateError(folder.name, "cookiecutter.json does not exist")
    questions = read_questions(folder.joinpath("cookiecutter.json"))

    obtain_user_input(questions)
    data = {"cookiecutter": {question.question_id: question.answer for question in questions}}

    template_path = obtain_template_path(folder)
    files = obtain_files(template_path, output_folder, data)

    template = Template(template_path, JinjaRenderer)
    for extension in EXTENSIONS:
        template.renderer.environment.add_extension(extension)
    template.add_files(files)

    data["cookiecutter"] |= {
        "_template": str(template.base_folder),
        "_repo_dir": str(template.base_folder),
        "_output_dir": str(output_folder),
    }
    template.push_data(data)

    return template
