from typing import Dict, Union


class Request:
    """
    Class for requesting variable to the user.
    """

    requests: Dict[str, Union[str, int, float]]
