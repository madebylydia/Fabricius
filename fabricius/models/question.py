import typing

from rich.prompt import Prompt, PromptBase

QuestionType = typing.TypeVar("QuestionType")


class Question(typing.Generic[QuestionType]):
    """
    The Question class represent a question that will be asked to the users in order to fill the
    data required for a template.
    """

    question_id: str
    """
    The question ID is a string that will be used to identify the question.

    It is meant to be used inside the template to identify the question, but the "help" field
    should rather be used to show the actual question to the user. It still will be used as a
    fallback if "help" is not defined.
    """

    help: str | None
    """
    The prompt that will be shown to the user.
    """

    prompt: type[PromptBase[QuestionType]] | None
    """
    The type of prompt we're looking for.
    """

    default: QuestionType | None
    """
    The default answer.
    """

    _answer: QuestionType | str | None

    def __init__(
        self,
        question: str,
        *,
        help: str | None = None,
        default: QuestionType | None = None,
        prompt: type[PromptBase[QuestionType]] | None = None,
    ) -> None:
        self.question_id = question
        self.help = help
        self.default = default
        self.prompt = prompt
        self._answer = None

    @property
    def answer(self) -> QuestionType | str | None:
        return self._answer

    def ask(self) -> QuestionType | str:
        """
        Prompt the question to the user.
        """
        # TODO: Rewrite this part to be more "consistent", we just put "prompt" for the dev purposes. For now...
        prompt = self.prompt or Prompt
        if self.default is not None:
            answer = prompt.ask(self.help or self.question_id, default=self.default)
        else:
            answer = prompt.ask(self.help or self.question_id)
        self._answer = answer
        return self._answer

    def get_answer(self) -> QuestionType:
        """
        Return the previous answer, or ask the question if not answered.
        """
        return self._answer or self.ask()
