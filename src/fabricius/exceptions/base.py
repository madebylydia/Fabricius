class FabriciusException(Exception):
    """An exception was raised inside Fabricius.

    All exceptions of Fabricius MUST subclass this exception.
    """

    def __init__(self, error: object | None = None) -> None:
        super().__init__(error or "Exception inside Fabricius. No specific error raised.")
