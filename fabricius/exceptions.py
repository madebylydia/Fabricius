import pathlib


class FabriciusError(Exception):
    """
    An error was raised inside Fabricius.

    All exceptions of the Fabricius library **must** subclass this exception.
    """

    def __init__(self, error: object | None = None) -> None:
        super().__init__(error or "Error inside Fabricius. No specific error raised.")


class MissingRequiredValueError(FabriciusError):
    """
    Exception raised when a required value was not set inside an object.
    """

    def __init__(self, instance: object, missing_value: str) -> None:
        """
        Parameters
        ----------
        instance : object
            The object that holds the missing value.
        missing_value : str
            The value that is not set.
        """
        super().__init__(
            f"{instance.__class__.__name__} is missing a required value to be set: "
            f"'{missing_value}'"
        )


class AlreadyCommittedError(FabriciusError):
    """
    A file has already been committed/persisted.
    """

    def __init__(self, file_name: str) -> None:
        """Parameters
        ----------
        file_name : str
            The file's name that has already been committed.
        """
        super().__init__(f"File '{file_name}' has already been committed.")


class ConflictError(FabriciusError):
    """
    Conflicting parameters between objects.

    This mean that Fabricius cannot continue its work because there would be a conflict between
    one or two objects.

    For example, this error can be raised when two files have the same name in the same
    destination folder.
    """

    def __init__(self, instance: object, reason: str) -> None:
        """
        Parameters
        ----------
        instance : object
            The conflicting object.
        reason : str
            The reason for the conflict.
        """
        super().__init__(f"Conflict error: {instance.__class__.__name__}: {reason}")


class ForgeError(FabriciusError):
    """
    The template/repository's forge file contains an error that must be resolved.
    """

    def __init__(self, path: pathlib.Path, key: str, reason: str) -> None:
        key_indicator = "Error in file" if key == "file" else f'Key "{key}"'
        super().__init__(f"Forge file ({path.resolve()}) has an error: {key_indicator}: {reason}")


class TemplateError(FabriciusError):
    """
    The template has an error that cannot be automatically handled by Fabricius.
    """

    def __init__(self, template_name: str, reason: str) -> None:
        """
        Parameters
        ----------
        template_name : str
            The name of the template that raised the error.
        reason : str
            The reason for the error.
        """
        super().__init__(f"{template_name}: {reason}")
