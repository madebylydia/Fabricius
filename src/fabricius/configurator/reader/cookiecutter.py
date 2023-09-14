import pathlib
import typing

import yaml

from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.universal import QuestionConfig, UniversalConfig
from fabricius.utils import sentence_case


class CookieCutterConfigReader(BaseReader[dict[str, typing.Any]]):
    def process(self) -> dict[str, typing.Any]:
        return yaml.safe_load(self.config_file.read_text())

    def to_universal(self, parsed_data: dict[str, typing.Any]) -> UniversalConfig:
        questions: list[QuestionConfig[typing.Any]] = []

        for key, value in parsed_data.items():
            question_help = sentence_case(value)
            questions.append(QuestionConfig(id=key, help=question_help, type=None, choices=None))

        return UniversalConfig(
            root=self.config_file.parent, destination=pathlib.Path("."), questions=questions
        )
