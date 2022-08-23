from typing import Optional


class FabriciusError(Exception):
    """
    An error was raised inside Fabricius.
    """

    def __init__(self, error: Optional[str] = None) -> None:
        """
        An error was raised inside Fabricius.
        """
        super().__init__(error or "Error inside Fabricius. No specific error raised.")


class NoContentError(FabriciusError):
    """
    The file does not have any content.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file does not have any content.
        """
        super().__init__(f"File '{file_name}' does not have content from a template.")


class NoDestinationError(FabriciusError):
    """
    The file does not know where to go.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file does not know where to go.
        """
        super().__init__(f"File '{file_name}' does not have a destination set.")


class AlreadyCommittedError(FabriciusError):
    """
    The file has already been committed/persisted.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file has already been committed/persisted.
        """
        super().__init__(f"File '{file_name}' has already been committed.")


class RepoAlreadyExistError(FabriciusError):
    """
    The repository already exists.
    """

    def __init__(self, repository: str) -> None:
        """
        The repository already exists.
        """
        super().__init__(f"Repository '{repository}' already exists.")


class IntegrityError(FabriciusError):
    """
    An integrity error was found in a template.
    """

    def __init__(self, template_name: str, error: str) -> None:
        """
        An integrity error was found in a template.
        """
        super().__init__(f"Integrity error in template '{template_name}': {error}")


class TemplateNotFound(FabriciusError, NotADirectoryError):
    """
    The template could not be found.
    """

    def __init__(self, template_name: str) -> None:
        super().__init__(
            f"Template '{template_name}' was not found or is not a folder."
        )
