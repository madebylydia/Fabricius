import inflection


def camel_case(text: str) -> str:
    """
    Return the text formatted in camel case

    Parameters
    ----------
    text: str
        The text you want to format.

    Returns
    -------
    str:
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
    text: str
        The text you want to format.

    Returns
    -------
    str:
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
    text: str
        The text you want to format.

    Returns
    -------
    str:
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
    text: str
        The text you want to format.

    Returns
    -------
    str:
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
    text: str
        The text you want to format.

    Returns
    -------
    str:
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
    text: str
        The text you want to format.

    Returns
    -------
    str:
        The formatted text.

    Example
    -------
    .. code-block:: python

       >>> my_text = "Some text"
       >>> sentence_case(my_text)
       'Some text'
    """
    has_ending_id: bool = False
    if text.endswith("_id"):
        has_ending_id = True

    result = inflection.humanize(text)
    if has_ending_id:
        result += " ID"
    return result
