import json
import os
import pathlib
import typing

from fabricius.configurator.reader.base import BaseReader
from fabricius.configurator.universal import QuestionConfig, UniversalConfig
from fabricius.exceptions.invalid_template.invalid_config import InvalidConfigException
from fabricius.utils import sentence_case


class CookieCutterExtra(typing.TypedDict):
    """Extra information needed for the CookieCutter builder."""

    _extensions: list[str]
    _jinja2_env_vars: dict[str, typing.Any]
    _copy_without_render: list[str]
    _new_lines: str | None
    __prompts__: dict[str, str | dict[str, str]]


class CookieCutterConfigReader(BaseReader[dict[str, typing.Any], CookieCutterExtra]):
    """The config reader for CookieCutter based templates."""

    def process(self) -> dict[str, typing.Any]:
        try:
            return json.loads(self.config_file.resolve().read_text())
        except json.JSONDecodeError as exception:
            raise InvalidConfigException(
                self.config_file, self, "Config file cannot be read as expected."
            ) from exception

    @staticmethod
    def _get_prompt(parsed_data: dict[str, typing.Any], key: str) -> str:
        # https://cookiecutter.readthedocs.io/en/stable/advanced/human_readable_prompts.html
        if not parsed_data.get("__prompts__"):
            return sentence_case(key)
        human_prompts = parsed_data["__prompts__"]
        if isinstance(human_prompts.get(key), dict):
            human_prompts[key].get("__prompt__", sentence_case(key))
        elif isinstance(human_prompts.get(key), str):
            return human_prompts.get(key, sentence_case(key))
        return sentence_case(key)

    def universalize(
        self, parsed_data: dict[str, typing.Any]
    ) -> UniversalConfig[CookieCutterExtra]:
        questions: list[QuestionConfig] = []

        for key, value in parsed_data.items():
            prompt = self._get_prompt(parsed_data, key)
            hidden = key.startswith("_")
            default = value if isinstance(value, str) else None

            if isinstance(value, list):
                value = typing.cast(list[str], value)
                questions.append(
                    QuestionConfig(
                        id=key,
                        help=None,
                        prompt=prompt,
                        type=None,
                        default=default,
                        hidden=hidden,
                        factory=None,
                        choices=value,
                    )
                )

            elif isinstance(value, bool):
                questions.append(
                    QuestionConfig(
                        id=key,
                        help=None,
                        prompt=prompt,
                        type=bool,
                        default=default,
                        hidden=hidden,
                        factory=None,
                        choices=None,
                    )
                )

            else:
                questions.append(
                    QuestionConfig(
                        id=key,
                        help=None,
                        prompt=prompt,
                        type=None,
                        default=default,
                        hidden=hidden,
                        factory=None,
                        choices=None,
                    )
                )

        return UniversalConfig(
            root=self.config_file.parent,
            destination=pathlib.Path(".").resolve(),
            questions=questions,
            extra=CookieCutterExtra(
                _extensions=parsed_data.get("_extensions", []),
                _jinja2_env_vars=parsed_data.get("_jinja2_env_vars", {}),
                _copy_without_render=parsed_data.get("_copy_without_render", []),
                _new_lines=parsed_data.get("_new_lines", os.linesep),
                __prompts__=parsed_data.get("__prompts__", {}),
            ),
        )
