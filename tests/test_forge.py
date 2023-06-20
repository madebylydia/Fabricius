import pathlib

import pytest

from fabricius.app.forge import Forge, ForgeV1
from fabricius.exceptions import ForgeError

TEST_FOLDER = pathlib.Path(__file__, "..")
META_FOLDER = TEST_FOLDER / "meta"
FORGE_FOLDER = META_FOLDER / "forge"
BASE_FORGE_V1 = FORGE_FOLDER / "v1" / "validation"


@pytest.fixture()
def forge() -> Forge:
    return Forge.from_adapter(ForgeV1(FORGE_FOLDER / "forge_complete.py"))


def will_raise(file: pathlib.Path, match: str):
    to_match = ForgeV1(file)
    with pytest.raises(ForgeError, match=match):
        to_match.validate()


def test_forge_v1_raw() -> None:
    PATH = TEST_FOLDER / "meta" / "forge" / "forge_v1_raw.py"

    forge = ForgeV1(PATH)

    assert forge.raw() == {"version": 1, "type": "repository"}


def test_forge_v1_validate_unknown_key() -> None:
    will_raise(BASE_FORGE_V1 / "unknown_key.py", "Key not valid / does not exist.")


def test_forge_v1_validate_missing_required_keys() -> None:
    will_raise(BASE_FORGE_V1 / "missing_required.1.py", "Not defined, but required")
    will_raise(BASE_FORGE_V1 / "missing_required.2.py", "Not defined, but required")


def test_forge_v1_validate_version() -> None:
    will_raise(
        BASE_FORGE_V1 / "wrong_version.py",
        "Adapter is for version 1, can't read a file that has version 2",
    )


def test_forge_v1_validate_type() -> None:
    will_raise(BASE_FORGE_V1 / "invalid_type.py", 'Must be "repository" or "template", not ".*"')


def test_forge_v1_validate_method() -> None:
    will_raise(BASE_FORGE_V1 / "invalid_method.py", 'Method must be "setup" or "run".')
    will_raise(
        BASE_FORGE_V1 / "method_in_repository.py",
        'Only usable in type "template", but this key is used in type "repository"',
    )


def test_forge_v1_validate_root() -> None:
    will_raise(
        BASE_FORGE_V1 / "invalid_root.py",
        "Type .* not accepted, must be one of: <class 'str'> <class 'pathlib.Path'>",
    )

    forge = ForgeV1(BASE_FORGE_V1 / "valid_root.py")
    forge.validate()

    data = Forge.from_adapter(forge)
    assert data.get_root_path() == BASE_FORGE_V1 / "templates"


def test_forge_v1_validate_templates() -> None:
    will_raise(
        BASE_FORGE_V1 / "invalid_templates.py",
        "Type .* not accepted, must be one of: <class 'list'>",
    )
    will_raise(
        BASE_FORGE_V1 / "templates_in_template.py",
        'Only usable in type "repository", but this key is used in type "template"',
    )

    forge = ForgeV1(BASE_FORGE_V1 / "valid_templates.py")
    forge.validate()

    data = Forge.from_adapter(forge)

    assert data.get_templates() == []
    assert data.get_templates(require_existence=False) == [
        pathlib.Path(BASE_FORGE_V1 / "templates" / "my_template")
    ]


def test_forge_root(forge: Forge) -> None:
    assert forge.get_root_path() == FORGE_FOLDER / "templates"


def test_forge_templates(forge: Forge):
    assert forge.get_templates() == []
    assert forge.get_templates(require_existence=False) == [
        FORGE_FOLDER / "templates" / "template_a"
    ]
