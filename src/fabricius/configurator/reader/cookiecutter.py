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
            if isinstance(value, list):
                value = typing.cast(list[str], value)
                questions.append(
                    QuestionConfig(
                        id=key, help=sentence_case(key), type=None, default=None, choices=value
                    )
                )
            elif isinstance(value, bool):
                questions.append(
                    QuestionConfig(
                        id=key, help=sentence_case(key), type=bool, default=value, choices=None
                    )
                )
            else:
                questions.append(
                    QuestionConfig(
                        id=key,
                        help=value or sentence_case(key),
                        type=None,
                        default=None,
                        choices=None,
                    )
                )

        return UniversalConfig(
            root=self.config_file.parent, destination=pathlib.Path("."), questions=questions
        )
