from fabricius.exceptions.base import FabriciusException


class SignalException(FabriciusException):
    """Raised when a hook run fails."""

    exit_code: int | None
    """The associated exit code of the exception, if any.
    Must be used when this exception is raised, the runtime won't stop by itself.
    """

    def __init__(
        self, signal: str, reason: str | None = None, *, exit_code: int | None = None
    ) -> None:
        super().__init__(
            f"Signal {signal} failed to run: {reason}"
            if reason
            else f"Signal {signal} has failed to run. No reason provided."
        )
        self.exit_code = exit_code
