"""
Utilities shipped with Fabricius.
"""
import typing
import inflection

from math import sqrt
from rich.color import Color


def calculate_text_color(color: Color, *, threshold: int = 150) -> "typing.Literal['black', 'bright_white']":
    """
    Calculate if the text should be in black or white depending on a color.
    It uses the following formula:
        (r * 0.299 + g * 0.587 + b * 0.114) > threshold
    Where r, g, and b are the RGB (triplet) values of the color.

    Parameters
    ----------
    color : str
        The color we're calculating against to.
        This must be an HEX color string, (Like this: "#000000")
    threshold : int
        The threshold to determine if the text is black or white.

    Raises
    ------
    AttributeError :
        The triplet is not defined in the color.

    Returns
    -------
    str :
        Return either "black" or "bright_white"
    """
    if not color.triplet:
        raise AttributeError("Missing triplet in color")
    r, g, b = tuple(color.triplet)

    return 'black' if (r * 0.299 + g * 0.587 + b * 0.114) > threshold else 'bright_white'  # type: ignore


def camel_case(text: str) -> str:
    """
    Return the text formatted in camel case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> camel_case(my_text)
       'someText'
    """
    return inflection.camelize(text, False)


def snake_case(text: str) -> str:
    """
    Return the text formatted in snake case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> snake_case(my_text)
       'some_text'
    """
    return inflection.underscore(text)


def dash_case(text: str) -> str:
    """
    Return the text formatted in dash case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> dash_case(my_text)
       'some-text'
    """
    return inflection.dasherize(text)


def pascal_case(text: str) -> str:
    """
    Return the text formatted in pascal case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> pascal_case(my_text)
       'SomeText'
    """
    return inflection.camelize(text, True)


def capital_case(text: str) -> str:
    """
    Return the text formatted in capital case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> capital_case(my_text)
       'Some Text'
    """
    return inflection.titleize(text)


def sentence_case(text: str) -> str:
    """
    Return the text formatted in sentence case

    Parameters
    ----------
    text : str
        The text you want to format.

    Returns
    -------
    str :
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> sentence_case(my_text)
       'Some text'
    """
    has_ending_id = bool(text.endswith("_id"))
    result = inflection.humanize(text)
    if has_ending_id:
        result += " ID"
    return result
