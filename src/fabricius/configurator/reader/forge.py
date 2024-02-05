import json

from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.types import ALL_EXPORTABLE_FORGE
from fabricius.configurator.universal import QuestionConfig, UniversalConfig
from fabricius.exceptions.invalid_template import InvalidConfigException
from fabricius.types import NoExtraDict


class ForgeConfigReader(BaseReader[ALL_EXPORTABLE_FORGE, NoExtraDict]):
    def process(self):
        return json.loads(self.config_file.read_text())

    def universalize(self, parsed_data: ALL_EXPORTABLE_FORGE) -> UniversalConfig[NoExtraDict]:
        try:
            if parsed_data["type"] == "repository":
                return UniversalConfig(
                    root=parsed_data["root"],
                    destination=parsed_data["root"],
                    questions=[],
                    extra={},
                )

            if parsed_data["type"] == "template":
                questions = [
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
                    for question in parsed_data["questions"]
                ]

                return UniversalConfig(
                    root=parsed_data["root"],
                    destination=parsed_data["root"],
                    questions=questions,
                    extra={},
                )

        except KeyError as exception:
            raise InvalidConfigException(
                self.config_file, type(self), f"Missing key: {exception}"
            ) from exception

        raise InvalidConfigException(
            self.config_file,
            type(self),
            f"Unknown forge type: {parsed_data['type']}",
        )
