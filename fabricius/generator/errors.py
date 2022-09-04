from fabricius.errors import FabriciusError


class NoContentError(FabriciusError):
    """
    The file does not have any content.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file does not have any content.
        """
        super().__init__(f"File '{file_name}' was not set with a content/template.")


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
