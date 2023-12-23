import json
import typing

from fabricius import exceptions
from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.types import ALL_EXPORTABLE_FORGE
from fabricius.configurator.universal import QuestionConfig, UniversalConfig


class ForgeExtra(typing.TypedDict):
    ...


class ForgeConfigReader(BaseReader[ALL_EXPORTABLE_FORGE, ForgeExtra]):
    def process(self):
        return json.loads(self.config_file.read_text())

    def to_universal(self, parsed_data: ALL_EXPORTABLE_FORGE) -> UniversalConfig[ForgeExtra]:
        if parsed_data["type"] == "repository":
            return UniversalConfig(
                root=parsed_data["root"], destination=parsed_data["root"], questions=[], extra={}
            )
        if parsed_data["type"] == "template":
            questions: list[QuestionConfig] = []

            for question in parsed_data["questions"]:
                questions.append(
                    QuestionConfig(
                        id=question["id"],
                        help=question.get("help"),
                        prompt=question.get("prompt"),
                        type=question.get("type"),
                        default=question.get("default"),
                        hidden=question.get("hidden", False),
                        factory=question.get("factory"),
                        choices=question.get("choices"),
                    )
                )

            return UniversalConfig(
                root=parsed_data["root"],
                destination=parsed_data["root"],
                questions=questions,
                extra={},
            )
        raise exceptions.InvalidForgeException(
            self.config_file,
        )
