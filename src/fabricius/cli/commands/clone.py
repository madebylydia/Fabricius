import pathlib

import click
from git import GitCommandError, Repo
from rich import get_console

from fabricius.app.config import Config
from fabricius.app.ui.progress_bar import ProgressBar
from fabricius.cli.exceptions import UserFeedbackError
from fabricius.cli.utils import pass_config
from fabricius.utils import snake_case


@click.command()
@click.argument("repository", type=click.STRING)
@click.argument("as_name", type=click.STRING, required=False, default=None)
@click.option(
    "--at",
    type=pathlib.Path,
    help=(
        "Where the cloned repository will be stored. If not indicated, it will be stored inside "
        "Fabricius's default download path."
    ),
    default=None,
)
@pass_config
def clone(config: Config, repository: str, as_name: str | None, *, at: pathlib.Path | None):
    """
    Download a repository and store it inside Fabricius.
    """
    console = get_console()

    alias = as_name if as_name is not None else snake_case(repository.lower().split("/")[-1])

    if alias in config.stored_repositories:
        raise UserFeedbackError(
            f"The alias [green]{alias}[/] already exists. Delete the repository first or use a "
            "different alias."
        )

    if at is None:
        at = config.download_path

    repo_local_path = (at / alias).resolve()

    with ProgressBar as progress:
        task_id = progress.add_task(f"Cloning {alias}...")

        def progress_callback(
            _: int, cur_count: str | float, max_count: str | float | None, message: str
        ) -> None:
            progress.update(
                task_id,
                completed=float(cur_count),
                total=float(max_count) if max_count else None,
                description=f"Cloning {alias}... {message}",
            )

        try:
            Repo.clone_from(repository, repo_local_path, progress=progress_callback)
        except GitCommandError as exception:
            raise UserFeedbackError(
                "Error cloning repository. Does a folder already exist?\n\nException details:\n"
                f"{exception}",
                exit_code=1,
            ) from exception

    config.stored_repositories[alias] = repo_local_path
    config.persist()

    console.print(
        f"Repository [green]{alias}[/] has been cloned and saved at {repo_local_path}.\n\n"
        "🌟 You can now use it with [red bold]fabricius build[/]."
    )
