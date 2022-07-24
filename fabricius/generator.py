from typing import List, Optional

from fabricius.contracts import GeneratorContract
from fabricius.contracts.file_generator import CommitResult
from fabricius.errors import AlreadyCommittedError
from fabricius.file import FileGenerator
from fabricius.reporter import Reporter


class Generator(GeneratorContract):
    reporter = Reporter()
    files = []

    def add_file(self, name: str, extension: Optional[str] = None):
        file = FileGenerator(name, extension)
        self.files.append(file)
        return file

    def execute(self, *, allow_overwrite: bool = False):
        result: List[CommitResult] = []
        for file in self.files:
            try:
                file_result = file.commit(overwrite=allow_overwrite)
                path = str(file_result["path"].absolute())
                if file_result["state"] == "persisted":
                    self.reporter.success(f"{path} ({file.name})", title="CREATED")
                elif file_result["state"] == "pending":
                    self.reporter.skip(f"{path} ({file.name})")
                result.append(file_result)
            except AlreadyCommittedError:
                self.reporter.skip(f"{file.name} - Already committed")
            except Exception:
                self.reporter.fail(file.name)
                self.reporter.console.print_exception(extra_lines=0)

        return result
