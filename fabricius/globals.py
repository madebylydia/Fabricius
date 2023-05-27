import typing
from threading import local

if typing.TYPE_CHECKING:
    from .app.main import App


_local = local()


def get_app() -> "App":
    try:
        return typing.cast("App", _local.app)
    except AttributeError as e:
        raise RuntimeError("App has not been set.") from e


def set_app(app: "App") -> None:
    _local.app = app
