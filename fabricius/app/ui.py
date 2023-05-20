import logging

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

    def _increase(self, file: File):
        if self.task is None:
            _log.warning("Progress or task not detected. Ignoring.")
            return
        self.progress.update(self.task, total=self.total_files, advance=1, description=file.name)

    def connect(self):
        after_file_commit.connect(self._increase)

    def disconnect(self):
        after_file_commit.disconnect(self._increase)
