import abc
import importlib.util
import logging
import pathlib
import types
import typing

import typing_extensions

from fabricius.app._forge_typing.v1 import UnknownForgeV1, UnknownQuestionV1
from fabricius.app.signals import __all__ as all_events
from fabricius.exceptions import FabriciusError, ForgeError

_log = logging.getLogger(__name__)
ReturnType = typing.TypeVar("ReturnType")


def execute_setup(path: pathlib.Path) -> typing.Any:
    _log.debug(f"Executing setup for path: {path.resolve()}")
    spec = importlib.util.spec_from_file_location(path.parent.name, path)
    if spec is None:
        raise FabriciusError(f'When loading "{path.resolve()}", spec not found.')
    if spec.loader is None:
        raise FabriciusError(f'When loading "{path.resolve()}", spec loader not found.')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "setup"):
        return module.setup()
    raise ForgeError(path, "file", '"setup" is not defined.')


plugin_signature = typing.Callable[..., typing.Any]


class ForgePlugin(typing.TypedDict, total=False):
    before_file_commit: plugin_signature | list[plugin_signature]
    on_file_commit_fail: plugin_signature | list[plugin_signature]
    after_file_commit: plugin_signature | list[plugin_signature]
    before_template_commit: plugin_signature | list[plugin_signature]
    after_template_commit: plugin_signature | list[plugin_signature]


class ForgeQuestion(typing.TypedDict):
    id: str
    help: str | None
    type: typing.Any | None
    choices: list[str]


class ForgeInit(typing.TypedDict):
    version: int
    type: typing.Literal["repository", "template"]
    root: pathlib.Path | None
    templates: list[str] | None
    questions: list[ForgeQuestion] | None
    plugins: ForgePlugin | None
    method: typing.Literal["run", "setup"]


class Forge:
    """
    A class that is used within Fabricius to interact with a Forge file.

    This should NOT be used by users, this is used in order to let Fabricius read required data in
    Fabricius.
    """

    _file: pathlib.Path
    """
    The path of the Forge file.
    """

    version: int
    """
    The version the forge.py is using.
    """

    type: typing.Literal["repository", "template"]
    """
    The type of content this forge file is linked to.
    """

    root: pathlib.Path | None
    """
    The used root path for reading templates/files.
    """

    templates: list[str] | None
    """
    The list of defined templates.
    """

    questions: list[ForgeQuestion] | None
    """
    A list of questions to prompt to the user.
    """

    plugins: ForgePlugin | None
    """
    A list of plugin to connect to Fabricius.
    """

    method: typing.Literal["run", "setup"]
    """
    The method to use to run the template.
    """

    def __init__(self, file: pathlib.Path, **kwargs: typing_extensions.Unpack[ForgeInit]) -> None:
        self._file = file
        self.version = kwargs["version"]
        self.type = kwargs["type"]
        self.root = kwargs["root"]
        self.templates = kwargs.get("templates")
        self.questions = kwargs.get("questions")
        self.plugins = kwargs.get("plugins")
        self.method = kwargs["method"]
        _log.debug(f"Forge's variables: {vars(self)}")

    def _for_type(self, forge_type: typing.Literal["repository", "template"]):
        if forge_type != self.type:
            raise ForgeError(
                self._file,
                "type",
                f'Only usable in type "{forge_type}", but this key is used in type "{self.type}"',
            )

    def __getitem__(self, key: str) -> typing.Any:
        return getattr(self, key)

    @property
    def is_template(self):
        return self.type == "template"

    @property
    def is_repository(self):
        return self.type == "repository"

    def get_root_path(self) -> pathlib.Path:
        root = pathlib.Path(self._file).parent
        if self.root:
            root = root / self.root
        _log.info("Final root path is %s", root)
        return root

    def get_templates(self, *, require_existence: bool = True) -> list[pathlib.Path]:
        templates: list[pathlib.Path] = []
        if not self.templates:
            return []
        root = self.get_root_path()
        for template in self.templates:
            path = root / template
            if not path.exists() and require_existence:
                _log.debug(
                    "%s does not exist (and require existence is True), continuing...", path
                )
                continue
            templates.append(path)
        _log.info("Found %s templates: %s", len(templates), templates)
        return templates

    @classmethod
    def from_adapter(cls, adapter: "ForgeAdapter[typing.Any]") -> "Forge":
        return cls(adapter.file, **adapter.build())


class ForgeAdapter(typing.Generic[ReturnType], metaclass=abc.ABCMeta):
    file: pathlib.Path

    version: typing.ClassVar[int]

    def __init__(self, file: pathlib.Path) -> None:
        self.file = file

    def _must_be(
        self,
        key: str,
        target: typing.Any,
        *target_types: type,
        optional: typing.Optional[bool] = False,
    ) -> None:
        if optional and target is None:
            return
        if not isinstance(target, target_types):
            raise ForgeError(
                self.file,
                key,
                f"Type {type(target)} not accepted, must be one of: "
                f'{" ".join(f"{target_type}" for target_type in target_types)}',
            )

    def _require_to_be(
        self,
        key: str,
        expected_type: typing.Literal["repository", "template"],
        actual_type: typing.Literal["repository", "template"],
    ) -> None:
        if expected_type != actual_type:
            raise ForgeError(
                self.file,
                key,
                f'Only usable in type "{expected_type}", but this key is used in type '
                f'"{actual_type}"',
            )

    @abc.abstractmethod
    def raw(self) -> ReturnType:
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def build(self) -> ForgeInit:
        raise NotImplementedError()


class ForgeV1(ForgeAdapter[UnknownForgeV1]):
    valid_keys = ["version", "type", "root", "templates", "questions", "plugins", "method"]

    version = 1

    def raw(self) -> UnknownForgeV1:
        """
        Returns the raw file of the ``forge.py``.
        """
        return execute_setup(self.file)

    def _validate_questions(self, questions: list[UnknownQuestionV1]) -> None:
        known_questions_id: list[str] = []
        for question in questions:
            q_id = self._validate_required(question, "id", str)
            if q_id in known_questions_id:
                raise ForgeError(
                    self.file,
                    f"questions.{q_id}.id",
                    f'Duplicate ID: Found same ID called "{q_id}"',
                )
            known_questions_id.append(q_id)

            help = question.get("help")
            self._must_be(f"questions.{q_id}.help", help, str, optional=True)

            q_type = question.get("type")
            self._must_be(f"questions.{q_id}.type", q_type, type, optional=True)

            choices = question.get("choices")
            self._must_be(f"questions.{q_id}.choices", choices, list, optional=True)

            if choices:
                for choice in choices:
                    if not isinstance(choice, str):
                        raise ForgeError(
                            self.file,
                            f"questions.{q_id}.choices",
                            'Choice must be a string, not "{type(choice)}"',
                        )

    def validate(self) -> None:
        """
        Verify that the given forge file is okay to work with.

        Raises
        ------
        fabricius.exceptions.ForgeError :
            The ``forge.py`` contains an error. More explanation in the traceback.
        """
        data = self.raw()

        ### General (Dict Keys) ###

        if invalid_keys := [key for key in data.keys() if key not in self.valid_keys]:
            raise ForgeError(self.file, invalid_keys[0], "Key not valid / does not exist.")

        ### Version ###

        version = self._validate_required(data, "version", int)
        if version != 1:
            raise ForgeError(
                self.file,
                "version",
                f"Adapter is for version 1, can't read a file that has version {version}",
            )

        ### Type ###

        forge_type = self._validate_required(data, "type", str)
        if forge_type not in ["repository", "template"]:
            raise ForgeError(
                self.file, "type", f'Must be "repository" or "template", not "{forge_type}"'
            )

        ### Method ###

        method = data.get("method")
        self._must_be("method", method, str, optional=True)

        if method:
            self._require_to_be("method", "template", forge_type)
            if method not in ["setup", "run"]:
                raise ForgeError(self.file, "method", 'Method must be "setup" or "run".')

        ### Root ###

        root = data.get("root")
        self._must_be("root", root, str, pathlib.Path, optional=True)

        ### Templates ###

        templates = data.get("templates")
        self._must_be("templates", templates, list, optional=True)

        if templates := typing.cast(list[typing.Any] | None, templates):
            self._require_to_be("templates", "repository", forge_type)
            if any(not isinstance(value, str) for value in templates):
                raise ForgeError(self.file, "templates", "Values must all be string.")

        ### Question ###

        questions = data.get("questions", None)
        self._must_be("questions", questions, list, optional=True)
        if questions:
            self._require_to_be("questions", "template", forge_type)
            questions = typing.cast(list[typing.Any], questions)
            if not all(isinstance(value, dict) for value in questions):
                raise ForgeError(self.file, "questions", "All questions must be a dictionary.")
            self._validate_questions(questions)

        ### Plugins ###

        plugins = data.get("plugins")
        self._must_be("plugins", plugins, dict, optional=True)
        if plugins:
            if not isinstance(plugins, dict):
                raise ForgeError(
                    self.file,
                    "plugins",
                    "Must be a dict. Key is the event, value is the function/list of functions "
                    "to call.",
                )
            plugins = typing.cast(dict[typing.Any, typing.Any], plugins)
            if invalid_signal := [key for key in plugins.keys() if key not in all_events]:
                raise ForgeError(
                    self.file, "plugins", f'Signal "{invalid_signal[0]}" does not exist.'
                )
            if not all(
                isinstance(value, (types.FunctionType, list)) for value in plugins.values()
            ):
                raise ForgeError(
                    self.file, "plugins", "All values must be callable, or a list of callable."
                )

    def _validate_required(
        self,
        data: UnknownForgeV1 | UnknownQuestionV1,
        key: str,
        *types: type,
        optional: bool = False,
    ) -> typing.Any:
        result = data.get(key)
        if not result:
            raise ForgeError(self.file, key, "Not defined, but required")
        self._must_be(key, result, *types, optional=optional)
        return result

    def build(self) -> ForgeInit:
        self.validate()

        data = self.raw()
        forge_type = typing.cast(typing.Any, data.get("type"))

        return {
            "version": 1,
            "type": forge_type,
            "root": data.get("root"),
            "templates": data.get("templates", []),
            "questions": data.get("questions", []),
            "plugins": data.get("plugins", {}),
            "method": data.get("method", "setup"),
        }


VERSION_MAP = {1: ForgeV1}


def read_forge(file: pathlib.Path) -> Forge:
    data = execute_setup(file)

    version = data["version"]
    forge = VERSION_MAP[version]

    return Forge.from_adapter(forge(file))
