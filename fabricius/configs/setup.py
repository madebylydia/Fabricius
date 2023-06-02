import typing

from fabricius.types import PathStrOrPath

plugin_signature = typing.Callable[..., typing.Any]


class PluginConnectable(typing.TypedDict, total=False):
    before_file_commit: plugin_signature | list[plugin_signature]
    on_file_commit_fail: plugin_signature | list[plugin_signature]
    after_file_commit: plugin_signature | list[plugin_signature]
    before_template_commit: plugin_signature | list[plugin_signature]
    after_template_commit: plugin_signature | list[plugin_signature]


class QuestionV1(typing.TypedDict, total=False):
    id: str
    """
    The question's ID.
    This is how you'll refer to the question's value in the template.
    """

    help: str | None
    """
    How the question will be rendered in the terminal when prompting.
    """

    type: typing.Any | None
    """
    Define what type the variable is.
    It'll attempt to convert the answer by initializing a new class. For example:

    .. code-block:: py

       question = {
           "id": "number",
           "help": "What number do you like the most?",
           "type": int
       }

       answer = "39"  # The answer will always be a string, unless a type is defined and we try to
                       # convert it.

       if kind := question["type"]:
           try:
               kind(answer)
           except ValueError:
               ...
    """

    choices: list[str]
    """
    A list of choice the user must pick.
    """


class SetupV1(typing.TypedDict, total=False):
    version: typing.Literal[1]

    type: typing.Literal["template", "repository"]
    """
    The type this forge file is associated to.
    """

    root: PathStrOrPath
    """
    Usable with type : template / repository

    The path where templates are located.
    """

    questions: list[QuestionV1]

    templates: list[str]
    """
    Usable with type : template

    A list of available templates in this repository, if any.
    """

    plugins: PluginConnectable
    """
    Usable with type : template / repository

    The list of plugins to connect.
    If used in a forge file that is of type repository, plugins defined in the repository will be
    loaded for all templates contained in the repository.
    """

    method: typing.Literal["run", "setup"]
    """
    Usable with : template

    The method to use to render the template, it can be:

    * run : Run a function called "run" in the forge.py file.
    * setup : Run the builtin Fabricius render mechanism using the data available in the setup
        function.
    """
