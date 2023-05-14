import typing

from fabricius.models.signal import Signal

if typing.TYPE_CHECKING:
    from fabricius.models.file import File, FileCommitResult
    from fabricius.models.template import Template

    def before_file_commit_hint(file: File):
        ...

    def on_file_commit_fail_hint(file: File):
        ...

    def after_file_commit_hint(file: File):
        ...

    def before_template_commit_hint(template: Template[typing.Any]):
        ...

    def after_template_commit_hint(
        template: Template[typing.Any], files_commits: list[FileCommitResult]
    ):
        ...

else:
    before_file_commit_hint = None
    on_file_commit_fail_hint = None
    after_file_commit_hint = None
    before_template_commit_hint = None
    after_template_commit_hint = None


before_file_commit = Signal(func_hint=before_file_commit_hint)
on_file_commit_fail = Signal(func_hint=on_file_commit_fail_hint)
after_file_commit = Signal(func_hint=after_file_commit_hint)

before_template_commit = Signal(func_hint=before_template_commit_hint)
after_template_commit = Signal(func_hint=after_template_commit_hint)
