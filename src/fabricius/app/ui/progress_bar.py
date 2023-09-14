from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

ProgressBar = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TextColumn("[progress.remaining]ETA:"),
    TimeRemainingColumn(compact=True),
    transient=True,
)
