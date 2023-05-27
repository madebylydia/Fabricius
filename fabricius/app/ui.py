import logging
from contextlib import contextmanager
from typing import Any, Generator

from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from fabricius.app.main import logging
from fabricius.app.signals import after_file_commit
from fabricius.models.file import File
from fabricius.types import FileCommitResult

_log = logging.getLogger(__name__)


class TemplateProgressBar:
    total_files: int
    """
    The total files to process.
    Used to be set as the maximum in the progress bar.
    """

    progress: Progress

    task: TaskID | None

    def __init__(self, total_files: int) -> None:
        self.total_files = total_files
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            transient=True,
        )
        self.task = None

    @contextmanager
    def begin(self, first_message: str) -> Generator[Progress, Any, None]:
        try:
            after_file_commit.connect(self._increase)
            self.task = self.progress.add_task(first_message, total=self.total_files)
            with self.progress as progress:
                yield progress
        finally:
            after_file_commit.disconnect(self._increase)
            self.progress.stop()

    def _increase(self, file: File, result: FileCommitResult) -> None:
        if self.task is None:
            _log.warning("Progress or task not detected. Ignoring.")
            return
        self.progress.update(self.task, advance=1, description=file.name)
