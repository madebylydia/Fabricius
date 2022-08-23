import pathlib
import platformdirs


def get_external_templates_path() -> pathlib.Path:
    return platformdirs.user_data_path("fabricius").joinpath("templates")

def get_config(*, create_if_no_exist: bool = True) -> pathlib.Path:
    """
    Obtain the ``config.json``'s file path.

    Parameters
    ----------
    create_if_no_exist : :py:class:`bool`
        Create the ``config.json`` file if it does not exist. Default to True.

    Raises
    ------
    :py:exc:`FileNotFoundError` :
        If ``config.json`` does not exist and that ``create_if_no_exist`` is on ``False``.

    Returns
    -------
    :py:class:`pathlib.Path` :
        The ``config.json``'s path.
    """

    path = platformdirs.user_config_path("fabricius").joinpath("config.json")
    if not path.exists():
        if not create_if_no_exist:
            raise FileNotFoundError("'config.json' does not exist.")
        path.parent.mkdir(parents=True)
        path.touch()
        path.write_text("{}")
    return path
