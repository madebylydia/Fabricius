import errno
import pathlib
import subprocess
import sys
import tempfile
import typing

from fabricius.composers.jinja import JinjaComposer
from fabricius.exceptions import SignalException
from fabricius.models.file import FileCommitResult
from fabricius.models.generator import Generator
from fabricius.types import Data

if typing.TYPE_CHECKING:
    import collections.abc

HOOKS = ["pre_prompt", "pre_gen_project", "post_gen_project"]


class AvailableHooks(typing.TypedDict):
    """A dict listing available hooks for a template."""

    pre_prompt: pathlib.Path | None
    pre_gen_project: pathlib.Path | None
    post_gen_project: pathlib.Path | None


def get_hooks(base_folder: pathlib.Path) -> AvailableHooks:
    hooks_folder = base_folder / "hooks"
    if not hooks_folder.exists():
        return AvailableHooks(pre_prompt=None, pre_gen_project=None, post_gen_project=None)

    available_hooks = AvailableHooks(pre_prompt=None, pre_gen_project=None, post_gen_project=None)
    for hook_file in hooks_folder.iterdir():
        # annoying mypy moment... requiring literal string...
        if hook_file.stem == "pre_prompt":
            available_hooks["pre_prompt"] = hook_file
        if hook_file.stem == "post_gen_project":
            available_hooks["post_gen_project"] = hook_file
        if hook_file.stem == "pre_gen_project":
            available_hooks["pre_gen_project"] = hook_file

    return available_hooks


def run_hook(hook: pathlib.Path, data: Data):
    # Renderer the file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=hook.suffix, mode="wb"
    ) as temporary_file:
        final_content = JinjaComposer().push_data(data).render(hook.read_text())
        temporary_file.write(final_content.encode("utf-8"))

    path = pathlib.Path(temporary_file.name).resolve()
    cmd = [sys.executable, str(path)] if hook.suffix == ".py" else [str(path)]

    try:
        with subprocess.Popen(cmd, shell=sys.platform.startswith("win"), cwd=".") as process:
            proc_exit = process.wait(10)
            if proc_exit != 0:
                raise SignalException(hook.name, f"Exit status: {proc_exit}")
    except OSError as exception:
        if exception.errno == errno.ENOEXEC:
            raise SignalException(
                hook.name, "Might be an empty file or missing a shebang"
            ) from exception
        raise SignalException(hook.name, f"Exception: {exception}") from exception


@typing.overload
def adapt(
    hook: pathlib.Path, hook_type: typing.Literal["pre_prompt"]
) -> "collections.abc.Callable[[Generator[JinjaComposer]], typing.Any]":
    ...


@typing.overload
def adapt(
    hook: pathlib.Path, hook_type: typing.Literal["pre"]
) -> "collections.abc.Callable[[Generator[JinjaComposer]], typing.Any]":
    ...


@typing.overload
def adapt(
    hook: pathlib.Path, hook_type: typing.Literal["post"]
) -> "collections.abc.Callable[[Generator[JinjaComposer], list[FileCommitResult]], typing.Any]":
    ...


def adapt(
    hook: pathlib.Path, hook_type: typing.Literal["pre_prompt", "pre", "post"]
) -> (
    "collections.abc.Callable[[Generator[JinjaComposer]], typing.Any]"
    | "collections.abc.Callable[[Generator[JinjaComposer], list[FileCommitResult]], typing.Any]"
):
    if hook_type == "pre_prompt":

        def pre_prompt_wrapper(template: Generator[JinjaComposer]):
            run_hook(hook, template.data)

        return pre_prompt_wrapper

    if hook_type == "pre":

        def pre_wrapper(template: Generator[JinjaComposer]):
            run_hook(hook, template.data)

        return pre_wrapper

    def post_wrapper(template: Generator[JinjaComposer], _: list[FileCommitResult]):
        run_hook(hook, template.data)

    return post_wrapper
