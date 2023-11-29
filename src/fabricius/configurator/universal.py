import dataclasses
import pathlib
import typing

from fabricius.exceptions import UserInputException


@dataclasses.dataclass(kw_only=True)
class QuestionConfig[QuestionType: type]:
    id: str
    """
    The "ID" of the question.

    This is what is used to fill the data's keys, and what should be used to refer to the
    question's value inside a template.
    """

    help: str | None
    """
    An optional help string to show to the user.

    This is what the terminal will output to the user.
    If None, the question's ID will be printed instead.
    """

    type: QuestionType | None
    """
    The type the question must be.

    Fabricius, will prompting the user, will attempt to convert the question's answer by
    attempting a class's initialization, like this:

    .. code:: python

       question = QuestionConfig(id="test", type=int)

       user_input = "123"
       # Do notice here, that this is a string, and not an integer, so conversion is needed.

       final_answer = question.answer("123")

       print(type(final_answer))
       # <type 'int'>
       # You don't need to know what ".answer" does, but it basically will do the conversion based
       # on what you've given as a type and make other checks.
    """

    choices: list[str] | None
    """
    A list of choices for the user to pick from.

    If None, the user is free to pass anything.
    """

    def validate(self, user_answer: str) -> QuestionType:
        """
        Attempt to return the expected output of the user's input (TL;DR get user's final answer)

        Parameters
        ----------
        user_answer : str
            The raw answer of the user.

        Returns
        -------
        TypeVar: _QT
            The associated type of the question.

        Raises
        ------
        fabricius.exceptions.UserInputException
            Raised when either the question is not contained into the list of choice, or the
            answer cannot be converted to the given type.
        """
        if self.choices and user_answer not in self.choices:
            raise UserInputException(user_answer, ", ".join(self.choices))
        if self.type:
            try:
                return self.type(user_answer)
            except TypeError as exception:
                raise UserInputException(user_answer, str(type(self.type))) from exception
        else:
            return typing.cast(QuestionType, user_answer)


@dataclasses.dataclass(kw_only=True)
class UniversalConfig:
    root: pathlib.Path
    """
    The source of the template.
    """

    destination: pathlib.Path
    """
    The given destination of the template.

    No extra sub-folders will be created.
    """

    questions: list[QuestionConfig[typing.Any]]
    """
    A list of questions to ask to the users.
    """
