import json
import typing

from fabricius import exceptions
from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.types import ALL_EXPORTABLE_FORGE
from fabricius.configurator.universal import QuestionConfig, UniversalConfig


class ForgeConfigReader(BaseReader[ALL_EXPORTABLE_FORGE]):
    def process(self):
        return json.loads(self.config_file.read_text())

    def to_universal(self, parsed_data: ALL_EXPORTABLE_FORGE) -> UniversalConfig:
        if parsed_data["type"] == "repository":
            return UniversalConfig(
                root=parsed_data["root"], destination=parsed_data["root"], questions=[]
            )
        if parsed_data["type"] == "template":
            questions: list[QuestionConfig[typing.Any]] = []

            for question in parsed_data["questions"]:
                questions.append(
                    QuestionConfig(
                        id=question["id"],
                        help=question["help"],
                        type=question["type"],
                        default=question["default"],
                        choices=question["choices"],
                    )
                )

            return UniversalConfig(
                root=parsed_data["root"], destination=parsed_data["root"], questions=questions
            )
        raise exceptions.InvalidForgeException(
            self.config_file,
        )
