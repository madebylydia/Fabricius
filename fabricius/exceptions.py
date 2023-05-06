class FabriciusError(Exception):
    """
    An error was raised inside Fabricius.
    """

    def __init__(self, error: object | None = None) -> None:
        """
        An error was raised inside Fabricius.
        """
        super().__init__(error or "Error inside Fabricius. No specific error raised.")


class MissingRequiredValueError(FabriciusError):
    """
    Exception raised when a required value was not set inside a class.
    """

    def __init__(self, instance: object, missing_attribute: str) -> None:
        """
        Exception raised when a required value was not set inside a class.
        """
        super().__init__(
            f"{instance.__class__.__name__} is missing a required value to be set: "
            f"'{missing_attribute}'"
        )


class AlreadyCommittedError(FabriciusError):
    """
    The file has already been committed/persisted.
    """

    def __init__(self, file_name: str) -> None:
        """
        The file has already been committed/persisted.
        """
        super().__init__(f"File '{file_name}' has already been committed.")


class ConflictError(FabriciusError):
    """
    Conflicting parameters between objects.
    """

    def __init__(self, instance: object, reason: str) -> None:
        super().__init__(f"Conflict error: {instance.__class__.__name__}: {reason}")


class TemplateError(FabriciusError):
    """
    The template has an error that cannot be handled by Fabricius.
    """

    def __init__(self, template_name: str, reason: str) -> None:
        super().__init__(f"{template_name}: {reason}")
