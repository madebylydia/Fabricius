import pathlib

import platformdirs


def get_external_templates_path() -> pathlib.Path:
    """
    Obtain the path to external templates.

    :meta private:
    """
    return platformdirs.user_data_path("fabricius").joinpath("templates")
