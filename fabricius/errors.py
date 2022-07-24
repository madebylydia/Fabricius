from typing import Optional


class FabriciusError(Exception):
    """
    An error was raised inside Fabricius.
    """

    def __init__(self, error: Optional[object] = None) -> None:
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
