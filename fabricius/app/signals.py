import typing

from fabricius.models.signal import Signal

if typing.TYPE_CHECKING:
    from fabricius.models.file import File, FileCommitResult
    from fabricius.models.generator import Generator

    def before_file_commit_hint(file: File):
        ...

    def on_file_commit_fail_hint(file: File):
        ...

    def after_file_commit_hint(file: File, result: FileCommitResult):
        ...

    def before_generator_commit_hint(template: Generator[typing.Any]):
        ...

    def after_generator_commit_hint(
        template: Generator[typing.Any], files_commits: list[FileCommitResult]
    ):
        ...

else:
    before_file_commit_hint = None
    on_file_commit_fail_hint = None
    after_file_commit_hint = None
    before_generator_commit_hint = None
    after_generator_commit_hint = None


before_file_commit = Signal(func_hint=before_file_commit_hint)
"""
A Signal called when a :py:obj:`File <fabricius.models.file.File>` is about to commit a file.
"""

on_file_commit_fail = Signal(func_hint=on_file_commit_fail_hint)
"""
A Signal called when a :py:obj:`File <fabricius.models.file.File>` had an exception occurring
when committing a file.
"""

after_file_commit = Signal(func_hint=after_file_commit_hint)
"""
A Signal called when a :py:obj:`File <fabricius.models.file.File>` has committed a file.
"""

before_generator_commit = Signal(func_hint=before_generator_commit_hint)
"""
A Signal called when a :py:obj:`Generator <fabricius.models.generator.Generator>` is about to commit
files.
"""

after_generator_commit = Signal(func_hint=after_generator_commit_hint)
"""
A Signal called when a :py:obj:`Generator <fabricius.models.generator.Generator>` has committed all
the files.
"""
