import base64
import logging
import typing

_log = logging.getLogger(__name__)
HASHED_CODE = (
    "aHR0cHM6Ly9iYzYzNTJkNGQxOTg1YTFlZmQ0YmI2NGMzYjFmZWFmZUBvNDQ1ODY0LmluZ2VzdC5zZW50cnkua"
    "W8vNDUwNjQ2MzExNjg1MzI0OA=="
)

try:
    import sentry_sdk

    sentry_sdk.init(
        dsn=base64.b64decode(HASHED_CODE).decode("utf-8"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
except ImportError:
    sentry_sdk = None
    _log.warning("Sentry is not installed. Error reporting is disabled.")


def can_report() -> bool:
    return sentry_sdk is not None


def report_exception(error: Exception, **kwargs: typing.Any) -> None:
    if sentry_sdk is None:
        return

    sentry_sdk.capture_exception(error, **kwargs)
    _log.info("Exception has been reported to Sentry.")
