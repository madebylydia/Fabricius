import json
import typing

from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.types import RepositoryV1, TemplateV1
from fabricius.configurator.universal import QuestionConfig, UniversalConfig


class ForgeConfigReader(BaseReader[RepositoryV1 | TemplateV1]):
    def process(self):
        return json.loads(self.config_file.read_text())

    def to_universal(self, parsed_data: RepositoryV1 | TemplateV1) -> UniversalConfig:
        questions: list[QuestionConfig[typing.Any]] = []

        for key, value in parsed_data.items():
            pass

        return UniversalConfig(root="", destination="", questions=[])

        # TODO: Make the universal config reader
