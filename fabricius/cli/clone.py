import pathlib
import random
from typing import Optional, Union

import click
import git
from rich import get_console
from rich.highlighter import Highlighter
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
)
from rich.text import Text

from fabricius.config import Config
from fabricius.internal_utils import get_external_templates_path

PROGRESS_BAR = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    "-",
    TextColumn("Speed: [red]{task.fields[speed]}[/red]"),
    "-",
    TextColumn("Code: [red]{task.fields[op_code]}[/red]"),
)
task_id: TaskID
progress: Progress


@click.command("clone")
@click.argument("template")
@click.option(
    "--alias",
    help="An alias for the given repository/template.",
    show_default="repository's name",
    type=str,
    required=False,
)
@click.option(
    "--at-path",
    help="Where to clone the repository.",
    type=pathlib.Path,
    default=lambda: get_external_templates_path(),
)
def cmd_clone(template: str, *, alias: Optional[str], at_path: pathlib.Path):
    """
    Clone an external repository.
    """
    console = get_console()
    config = Config.get_config()

    def progress_bar(
        op_code: int,
        cur_count: Union[str, float],
        max_count: Union[str, float, None] = None,
        message: str = "",
    ):
        global task_id
        global progress
        progress.start_task(task_id)
        progress.update(
            task_id,
            total=float(max_count) if max_count else None,
            completed=float(cur_count),
            speed=message or "[bright_black]/",
            op_code=op_code,
        )
        if op_code == 66:
            # End of download
            progress.update(task_id, description="[green]Cloned!")

    repo_name = template.split("/")[-1]
    alias = alias or repo_name

    global progress
    with PROGRESS_BAR as progress:
        global task_id
        task_id = progress.add_task(
            f"[yellow]Cloning {repo_name}...", start=False, speed="[bright_black]/", op_code=0
        )
        repo = git.Repo.clone_from(template, at_path.joinpath(alias), progress_bar)

    config.save_repo(repo)
    config.save()

    you_like_it_you_have_it = [
        ":star-emoji:",
        ":sparkles-emoji:",
        ":smiling_face_with_heart-eyes-emoji:",
        ":glowing_star-emoji:",
        ":gem-emoji:",
        ":open_mouth-emoji:",
        ":muscle-emoji:",
        ":exploding_head-emoji:",
        ":thumbs_up-emoji:",
        ":sparkling_heart-emoji:",
        ":smiling_face_with_sunglasses-emoji:",
        ":smiley-emoji:",
        ":bulb-emoji:",
    ]

    class RainbowHighlighter(Highlighter):
        def highlight(self, text: Text):
            for index in range(len(text)):
                text.stylize(f"color({random.randint(16, 255)})", index, index + 1)

    rainbow = RainbowHighlighter()

    console.print(
        f"{random.choice(you_like_it_you_have_it)} {rainbow('Awesome!')} {random.choice(you_like_it_you_have_it)} We cloned [red]{alias}[/red] and is now ready to be used! Have fun! :D"
    )
