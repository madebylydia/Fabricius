import importlib.util
import pathlib
import typing

from fabricius.configs.internals import ALL_CONFIGS
from fabricius.configs.internals.forge_v1 import RepositoryV1, TemplateV1
from fabricius.configs.setup import QuestionV1
from fabricius.exceptions import FabriciusError, ForgeError

plugin_signature = typing.Callable[..., typing.Any]


def _read_repo_v1(path: pathlib.Path, forge_data: dict[str, typing.Any]) -> RepositoryV1:
    templates = forge_data.get("templates")
    if templates is None:
        raise ForgeError(path, "templates", "No templates defined.")
    if not isinstance(templates, list):
        raise ForgeError(path, "templates", "Must be a list of str that represent templates path")

    return RepositoryV1(version=1, type="repository", root=path, templates=templates)


def _read_questions(
    path: pathlib.Path, questions: list[dict[str, typing.Any]]
) -> list[QuestionV1]:
    to_return_questions: list[QuestionV1] = []
    for question in questions:
        q_id = question.get("id")
        if q_id is None:
            raise ForgeError(path, "questions.id", "Must give an ID to the question")
        if question.get("help") and not isinstance(question["help"], str):
            raise ForgeError(path, f"questions.{q_id}.help", "Help must be a string")
        if choices := question.get("choices", []):
            if not isinstance(choices, list):
                raise ForgeError(
                    path, f"questions.{q_id}.choices", "Choices must be a list of string"
                )
            for choice in choices:
                if not isinstance(choice, str):
                    raise ForgeError(
                        path,
                        f"questions.{q_id}.choices",
                        f"Choices must all be string, not {type(choice)}",
                    )

        to_return_questions.append(
            QuestionV1(
                id=q_id,
                help=question.get("help"),
                type=question.get("type"),
                choices=question.get("choices", []),
            )
        )
    return to_return_questions


def _read_template_v1(path: pathlib.Path, forge_data: dict[str, typing.Any]) -> TemplateV1:
    method = forge_data.get("method", "setup")
    if method not in ["setup", "run"]:
        raise ForgeError(path, "method", f'Must be "setup" or "run", not {method}')
    questions = forge_data.get("questions")
    if questions and not isinstance(questions, list):
        raise ForgeError(path, "questions", "Must be a list of dict.")

    return TemplateV1(
        version=1,
        type="template",
        root=path,
        method=method,
        questions=_read_questions(path, forge_data.get("questions", [])),
    )


def execute_setup(path: pathlib.Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.parent.name, path)
    if spec is None:
        raise FabriciusError(f'When loading "{path.resolve()}", spec not found.')
    if spec.loader is None:
        raise FabriciusError(f'When loading "{path.resolve()}", spec loader not found.')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "setup"):
        return module.setup()
    raise ForgeError(path, "File", '"setup" is not defined.')


def read_forge_file(path: pathlib.Path) -> ALL_CONFIGS:
    setup_data = execute_setup(path)

    if not isinstance(setup_data, dict):
        raise ForgeError(path, "File", '"setup" does not export a dict.')

    if setup_data.get("type") is None:
        raise ForgeError(path, "type", "Type not defined.")

    # sourcery skip: merge-nested-ifs
    if setup_data.get("type") == "repository":
        if setup_data["version"] == 1:
            return _read_repo_v1(path, setup_data)
    if setup_data.get("type") == "template":
        if setup_data["version"] == 1:
            return _read_template_v1(path, setup_data)
