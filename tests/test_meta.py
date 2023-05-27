import re

from fabricius import __version__ as fabricius_version
from fabricius.utils import calculate_text_color


def test_version_is_semantic():
    # I hope the guy who made this regex rests in peace.
    regex = re.match(
        r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
        fabricius_version,
    )
    print(regex)
    assert regex is not None, "Your version is not semantic."


def test_color_calculation():
    assert calculate_text_color("black") == "bright_white"
    assert calculate_text_color("bright_white") == "black"
