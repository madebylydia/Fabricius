from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

ProgressBarNoText = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    transient=True,
)
"""
A progress bar with a description.
Does not add additional text/information.
"""

ProgressBar = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TextColumn("[progress.remaining]ETA:"),
    TimeRemainingColumn(compact=True),
    transient=True,
)
"""
A progress bar with a description and expected ETA.
"""
