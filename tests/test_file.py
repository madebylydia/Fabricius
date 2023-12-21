import os
import pathlib
import stat
import sys
import typing
import uuid

import pytest

from fabricius.composers import (
    ChevronComposer,
    JinjaComposer,
    PythonFormatComposer,
    StringTemplateComposer,
)
from fabricius.exceptions import PreconditionException
from fabricius.exceptions.commit_exception.file_commit_exception import (
    FileCommitException,
)
from fabricius.models.file import File, FileCommitResult
from fabricius.signals import (
    after_file_commit,
    before_file_commit,
    on_file_commit_fail,
    on_file_deleted,
)

from .utils import TEST_ROOT


@pytest.fixture
def file() -> File:
    return File(f"{uuid.uuid4()}", "txt")


def fill_fake_information(file: File, tmp_path: pathlib.Path):
    file.to_directory(tmp_path)
    file.from_content("Hello World")
    file.with_data({"foo": "bar"})


def test_file_read_file(file: File):
    assert file.content is None
    file.from_file(TEST_ROOT / "assets" / "test_file" / "test_file_read_file.txt")
    assert isinstance(file.content, str)
    assert "Hello {name}." == file.content.strip()


def test_file_read_from_content(file: File):
    assert file.content is None
    file.from_content("Hello {name}.")
    assert file.content == "Hello {name}."


def test_file_to_directory(file: File, tmp_path: pathlib.Path):
    with pytest.raises(NotADirectoryError):
        assert file.destination is None
        file.to_directory(__file__)

    file.to_directory(tmp_path)
    assert file.destination == tmp_path


def test_file_compute_destination(file: File, tmp_path: pathlib.Path):
    with pytest.raises(PreconditionException):
        assert file.destination is None
        file.compute_destination()

    file.to_directory(tmp_path)
    assert file.compute_destination() == tmp_path / f"{file.name}"


def test_file_use_composer(file: File):
    assert type(file.composer) is PythonFormatComposer
    file.use_string_template()
    assert type(file.composer) is StringTemplateComposer
    file.use_mustache()
    assert type(file.composer) is ChevronComposer
    file.use_jinja()
    assert type(file.composer) is JinjaComposer

    file.with_composer(PythonFormatComposer())
    assert type(file.composer) is PythonFormatComposer


def test_file_with_data_overwrite(file: File):
    assert file.data == {}
    file.with_data({"foo": "bar"})
    assert file.data == {"foo": "bar"}
    file.with_data({"fizz": "buzz"})
    assert file.data == {"fizz": "buzz"}


def test_file_with_data_no_overwrite(file: File):
    assert file.data == {}
    file.with_data({"foo": "bar"})
    assert file.data == {"foo": "bar"}
    file.with_data({"fizz": "buzz"}, overwrite=False)
    assert file.data == {"foo": "bar", "fizz": "buzz"}


def test_file_fake(file: File):
    assert not file.will_fake
    file.fake(True)
    assert file.will_fake
    file.fake(False)
    assert not file.will_fake


def test_file_overwrite(file: File):
    assert not file.should_overwrite
    file.overwrite(True)
    assert file.should_overwrite
    file.overwrite(False)
    assert not file.should_overwrite


def test_file_generate(file: File):
    with pytest.raises(PreconditionException):
        assert file.content is None
        file.generate()

    file.from_content("Hello {name}.").with_data({"name": "Jacques"})
    assert file.generate() == "Hello Jacques."

    file = (
        File(f"{uuid.uuid4()}", "txt")
        .use_string_template()
        .from_content("Hello $name.")
        .with_data({"name": "Jacques"})
    )
    assert file.generate() == "Hello Jacques."

    file = (
        File(f"{uuid.uuid4()}", "txt")
        .use_mustache()
        .from_content("Hello {{name}}.")
        .with_data({"name": "Jacques"})
    )
    assert file.generate() == "Hello Jacques."


def test_file_commit_preconditions(file: File, tmp_path: pathlib.Path):
    with pytest.raises(PreconditionException):
        assert file.destination is None
        file.commit()
    file.to_directory(tmp_path)

    with pytest.raises(PreconditionException):
        assert file.content is None
        file.commit()
    file.from_content("Hello {name}.")


@pytest.mark.parametrize("state", ["processing"])
def test_file_commit_precondition_state(
    file: File,
    tmp_path: pathlib.Path,
    state: typing.Literal["processing"],
):
    fill_fake_information(file, tmp_path)
    with pytest.raises(FileCommitException):
        file.state = state
        file.commit()


def test_file_commit_file_exist_no_overwrite(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    tmp_path.joinpath(file.name).touch()

    with pytest.raises(FileExistsError):
        file.commit()


def test_file_commit(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    file.overwrite(True)
    result = file.commit()
    assert isinstance(result, dict)
    assert result.keys() == FileCommitResult.__required_keys__
    assert file.state == "persisted"


def test_file_commit_create_parents_folder(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    path = tmp_path / "foo" / "bar" / "baz"
    file.to_directory(path)
    file.commit()
    assert path.exists()


def test_file_commit_fake(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    file.fake(True)
    result = file.commit()
    assert file.state == "persisted"
    assert result["destination"].exists() is False


def test_file_commit_signals(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)

    before_called = False
    after_called = False

    def signal_handler_before(file: File):
        nonlocal before_called
        before_called = True

    def signal_handler_after(file: File, result: FileCommitResult):
        nonlocal after_called
        after_called = True

    before_file_commit.connect(signal_handler_before)
    after_file_commit.connect(signal_handler_after)

    assert before_called is False
    assert after_called is False

    file.commit()

    assert before_called is True
    assert after_called is True


@pytest.mark.skipif(os.name == "nt", reason="Windows not supported (To be resolved)")
def test_file_commit_fail(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    old_permissions = tmp_path.stat().st_mode
    tmp_path.chmod(stat.S_IREAD)
    has_failed = False

    def signal_handler_fail(file: File):
        nonlocal has_failed
        has_failed = True

    on_file_commit_fail.connect(signal_handler_fail)
    file.commit()
    assert file.state == "failed"
    assert has_failed is True

    tmp_path.chmod(old_permissions)


def test_file_delete_file_not_exist(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)
    with pytest.raises(FileNotFoundError):
        file.delete()


def test_file_delete(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)

    file.commit()
    assert file.state == "persisted"
    assert file.compute_destination().exists() is True

    file.delete()
    print(file.__dict__)
    assert file.state == "deleted"
    assert file.compute_destination().exists() is False


def test_file_delete_signal(file: File, tmp_path: pathlib.Path):
    fill_fake_information(file, tmp_path)

    file.commit()
    assert file.state == "persisted"
    assert file.compute_destination().exists() is True

    was_called = False

    def signal_handler(file: File):
        nonlocal was_called
        was_called = True

    on_file_deleted.connect(signal_handler)

    file.delete()
    assert file.state == "deleted"
    assert was_called is True
