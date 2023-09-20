import click
from rich import get_console
from rich.prompt import Confirm

from fabricius.app.config import Config
from fabricius.app.ui.progress_bar import ProgressBarNoText
from fabricius.exceptions.user_feedback_error import UserFeedbackError
from fabricius.utils import force_rm


@click.command()
@click.argument("alias", type=click.STRING, help="The name of the repository to delete.")
@click.option(
    "-y",
    "--yes",
    "no_confirm",
    type=click.BOOL,
    is_flag=True,
    help="Skip the confirm prompt if this flag is given.",
)
def delete(alias: str, *, no_confirm: bool = False):
    """
    Delete a downloaded repository.
    """
    console = get_console()

    config = Config.get()

    if alias not in config.stored_repositories:
        raise UserFeedbackError(f"Repository [green]{alias}[/] does not exists.")

    repo_local_path = config.stored_repositories[alias]

    if not no_confirm:
        if not Confirm.ask(
            f"Are you sure you'd like to delete [green]{alias}[/] at [green]{repo_local_path}[/]?"
        ):
            # Answered no
            return

    with ProgressBarNoText as progress:
        progress.add_task("Deleting...", total=None)
        force_rm(repo_local_path)

    del config.stored_repositories[alias]
    config.persist()

    console.print(f"Repository [green]{alias}[/] has been deleted.")
