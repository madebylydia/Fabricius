import typing

from fabricius.models.signal import Signal

if typing.TYPE_CHECKING:
    from fabricius.models.file import File, FileCommitResult
    from fabricius.models.generator import Generator

    def before_file_commit_hint(file: File):
        ...

    def after_file_commit_hint(file: File, result: FileCommitResult):
        ...

    def before_generator_start_hint(generator: Generator):
        ...

    def after_generator_start_hint(generator: Generator):
        ...

    def on_file_commit_fail_hint(file: File):
        ...

else:
    before_file_commit_hint = None
    after_file_commit_hint = None
    before_generator_start_hint = None
    after_generator_start_hint = None
    on_file_commit_fail_hint = None


before_file_commit = Signal(func_hint=before_file_commit_hint)
after_file_commit = Signal(func_hint=after_file_commit_hint)

before_generator_start = Signal(func_hint=before_generator_start_hint)
after_generator_start = Signal(func_hint=after_generator_start_hint)

on_file_commit_fail = Signal(func_hint=on_file_commit_fail_hint)
