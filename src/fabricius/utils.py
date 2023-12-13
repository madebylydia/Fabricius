import os
import shutil
import stat
import typing

import inflection
from rich.color import Color

if typing.TYPE_CHECKING:
    import pathlib

    from _typeshed import StrOrBytesPath


class DictAllowMiss(dict[str, typing.Any]):
    """
    A subclass of Dict to return an empty string in case of missing key, instead of raising an
    error, so that it can play nice with composers.

    :meta private:
    """

    def __missing__(self, _: str) -> typing.Literal[""]:
        return ""


def contains_files(path: "pathlib.Path") -> bool:
    """
    Check if a directory contains files.

    Parameters
    ----------
    path : :py:class:`pathlib.Path`
        The path to check.

    Returns
    -------
    :py:class:`bool` :
        True if the directory contains files, False otherwise.
    """
    if not path.exists():
        return False
    return any(path.iterdir())


def deep_merge(
    to_dict: typing.Mapping[typing.Any, typing.Any],
    from_dict: typing.Mapping[typing.Any, typing.Any],
) -> typing.Mapping[typing.Any, typing.Any]:
    """
    Deeply merges two dictionaries. If a key from original dictionary is conflicting, value from
    the dict we copy from is preferred.

    Parameters
    ----------
    original : :py:class:`dict`
        The original dictionary.
    copy_from : :py:class:`dict`
        The dictionary we copy from.

    Returns
    -------
    :py:class:`dict` :
        A new dictionary that is the result of merging both dictionaries.
    """

    merged_dict = to_dict.copy()

    for key, value in from_dict.items():
        if key in merged_dict:
            if isinstance(merged_dict[key], dict) and isinstance(value, dict):
                merged_dict[key] = deep_merge(merged_dict[key], value)  # type: ignore
            else:
                merged_dict[key] = value
        else:
            merged_dict[key] = value

    return merged_dict


def calculate_text_color(
    color: str | Color, *, threshold: int = 150
) -> typing.Literal["black", "bright_white"]:
    """
    Calculate if the text should be in black or white depending on a color.
    It uses the following formula: (r * 0.299 + g * 0.587 + b * 0.114) > threshold
    Where r, g, and b are the RGB (triplet) values of the color.

    Parameters
    ----------
    color : :py:class:`str` or :py:class:`rich.Color`
        The color we're calculating against to.
        This must be a Color class (From Rich)
    threshold : :py:class:`int`
        The threshold to determine if the text is black or white.

    Raises
    ------
    :py:exc:`rich.color.ColorParseError` :
        If ``color`` is of type :py:class:`str`, this will try to parse the color, this error
        will be raised if failed to be parsed.

    Returns
    -------
    str :
        Return either "black" or "bright_white".
    """
    if isinstance(color, str):
        color = Color.parse(color)
    r, g, b = tuple(color.get_truecolor())

    return "black" if (r * 0.299 + g * 0.587 + b * 0.114) > threshold else "bright_white"


def camel_case(text: str) -> str:
    """
    Return the text formatted in camel case

    Parameters
    ----------
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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
    text : :py:class:`str`
        The text you want to format.

    Returns
    -------
    :py:class:`str` :
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


def force_rm(path: "StrOrBytesPath"):
    """
    A modified version of rmtree, which allow for removal of directory that contains git files.

    Parameters
    ----------
    path : :py:class:`str` or :py:class:`bytes`
        The path to remove.

    Raises
    ------
    :py:exc:`OSError` :
        If the path is not a directory.
    :py:exc:`PermissionError` :
        If the path is not writable.

    """

    def on_rmtree_exception(_: typing.Callable[..., typing.Any], path: str, __: typing.Any):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    shutil.rmtree(path, onerror=on_rmtree_exception)
