from fabricius.exceptions import FabriciusError


class FailedHookError(FabriciusError):
    """
    Raised when a hook run fails.
    """

    exit_code: int | None

    def __init__(
        self, hook: str, reason: str | None = None, *, exit_code: int | None = None
    ) -> None:
        super().__init__(
            f"Hook {hook} failed to run: {reason}"
            if reason
            else f"Hook {hook} has failed to run. No reason provided."
        )
        self.exit_code = exit_code
