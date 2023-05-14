import errno
import pathlib
import subprocess
import sys
import tempfile
import typing

from fabricius.models.file import FileCommitResult
from fabricius.models.template import Template
from fabricius.readers.cookiecutter.exceptions import FailedHookError
from fabricius.renderers.jinja_renderer import JinjaRenderer
from fabricius.types import Data

HOOKS = ["pre_gen_project", "post_gen_project"]


class AvailableHooks(typing.TypedDict):
    pre_gen_project: typing.Optional[pathlib.Path]
    post_gen_project: typing.Optional[pathlib.Path]


def get_hooks(base_folder: pathlib.Path) -> AvailableHooks | None:
    hooks_folder = base_folder.joinpath("hooks")
    if not hooks_folder.exists():
        return None

    available_hooks: AvailableHooks = {"post_gen_project": None, "pre_gen_project": None}
    for hook_file in hooks_folder.iterdir():
        # annoying mypy moment... requiring literal string...
        if hook_file.stem == "post_gen_project":
            available_hooks["post_gen_project"] = hook_file
        if hook_file.stem == "pre_gen_project":
            available_hooks["pre_gen_project"] = hook_file

    return None if len(available_hooks) == 0 else available_hooks


def run_hook(hook: pathlib.Path, data: Data):
    # Renderer the file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=hook.suffix, mode="wb"
    ) as temporary_file:
        final_content = JinjaRenderer(data).render(hook.read_text())
        temporary_file.write(final_content.encode("utf-8"))

    path = pathlib.Path(temporary_file.name).resolve()
    cmd = [sys.executable, str(path)] if hook.suffix == ".py" else [str(path)]

    try:
        proc_exit = subprocess.Popen(cmd, shell=sys.platform.startswith("win"), cwd=".").wait(10)
        if proc_exit != 0:
            raise FailedHookError(hook.name, f"Exit status: {proc_exit}")
    except OSError as exception:
        if exception.errno == errno.ENOEXEC:
            raise FailedHookError(
                hook.name, "Might be an empty file or missing a shebang"
            ) from exception
        raise FailedHookError(f"Exception: {exception}") from exception


@typing.overload
def adapt(
    hook: pathlib.Path, type: typing.Literal["pre"]
) -> typing.Callable[[Template[typing.Any]], typing.Any]:
    ...


@typing.overload
def adapt(
    hook: pathlib.Path, type: typing.Literal["post"]
) -> typing.Callable[[Template[typing.Any], list[FileCommitResult]], typing.Any]:
    ...


def adapt(
    hook: pathlib.Path, type: typing.Literal["pre", "post"]
) -> (
    typing.Callable[[Template[typing.Any]], typing.Any]
    | typing.Callable[[Template[typing.Any], list[FileCommitResult]], typing.Any]
):
    if type == "pre":

        def pre_wrapper(template: Template[typing.Any]):
            run_hook(hook, template.data)

        return pre_wrapper

    if type == "post":

        def post_wrapper(template: Template[typing.Any], files_commit: list[FileCommitResult]):
            run_hook(hook, template.data)

        return post_wrapper
