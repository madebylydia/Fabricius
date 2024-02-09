import pathlib
import typing

import pytest

from fabricius.composers.format import PythonFormatComposer
from fabricius.exceptions import PreconditionException
from fabricius.exceptions.commit_exception.file_commit_exception import (
    FileCommitException,
)
from fabricius.models.file import File
from fabricius.models.generator import Generator

Gen: typing.TypeAlias = Generator[PythonFormatComposer]


@pytest.fixture
def generator() -> Gen:
    return Generator(PythonFormatComposer())


def test_generator_add_file(generator: Gen):
    """Test that the generator's fake function."""
    file = File("test.txt")
    generator.add_file(file)
    assert generator.files == [file]


def test_generator_add_files(generator: Gen):
    """Test that the generator's fake function."""
    files = [File("test.txt"), File("test2.txt")]
    generator.add_files(*files)
    assert generator.files == files


def test_generator_to_directory(generator: Gen):
    """Test that the generator's fake function."""
    with pytest.raises(PreconditionException):
        generator.to_directory(__file__)

    existing_path = pathlib.Path(__file__, "..").resolve()
    generator.to_directory(existing_path)
    assert generator.destination == existing_path

    unexisting_path = existing_path / "i_do_not_exist"
    generator.to_directory(unexisting_path)
    assert generator.destination == unexisting_path
    assert not unexisting_path.exists()


def test_generator_pass_data_to_file(generator: Gen):
    """Test that the generator's fake function."""
    assert generator.data == {}
    generator.to_directory(pathlib.Path(__file__, "..").resolve())
    generator.with_data({"foo": "bar"})
    generator.add_file(File("test.txt"))
    file = generator.compiled_files[0]
    assert file.data == {"foo": "bar"}


def test_generator_execution_fake(generator: Gen, tmp_path: pathlib.Path):
    """Test that the generator's execution function."""
    files = [
        File("test.txt").from_content("File 1 content: {name}"),
        File("test2.txt").from_content("File 2 content: {name}"),
    ]
    generator.add_files(*files)
    generator.to_directory(tmp_path)
    generator.with_data({"name": "Michael"})
    generator.fake(True)
    generator.execute()
    assert not (tmp_path / "test.txt").exists()


def test_generator_execution(generator: Gen, tmp_path: pathlib.Path):
    """Test that the generator's execution function."""
    files = [
        File("test.txt").from_content("File 1 content: {name}"),
        File("test2.txt").from_content("File 2 content: {name}"),
    ]
    generator.add_files(*files)
    generator.to_directory(tmp_path)
    generator.with_data({"name": "Michael"})

    generator.execute()

    assert (tmp_path / "test.txt").exists()
    assert (tmp_path / "test2.txt").exists()
    assert (tmp_path / "test.txt").read_text() == "File 1 content: Michael"
    assert (tmp_path / "test2.txt").read_text() == "File 2 content: Michael"


def test_generator_overwrite(generator: Gen, tmp_path: pathlib.Path):
    """Test that the generator's overwrite function."""
    files = [
        File("test.txt").from_content("File 1 content: {name}"),
        File("test2.txt").from_content("File 2 content: {name}"),
    ]
    generator.add_files(*files)
    generator.to_directory(tmp_path)
    generator.with_data({"name": "Michael"})

    (tmp_path / "test.txt").write_text("I must not be overwritten")

    assert (tmp_path / "test.txt").exists()
    assert not (tmp_path / "test2.txt").exists()

    with pytest.raises(PreconditionException):
        generator.execute()

    assert (tmp_path / "test.txt").read_text() == "I must not be overwritten"
    assert not (tmp_path / "test2.txt").exists()

    generator.overwrite(True)
    generator.execute()

    assert (tmp_path / "test.txt").exists()
    assert (tmp_path / "test2.txt").exists()
    assert (tmp_path / "test.txt").read_text() == "File 1 content: Michael"
    assert (tmp_path / "test2.txt").read_text() == "File 2 content: Michael"


def test_generator_atomicity(generator: Gen, tmp_path: pathlib.Path):
    """Test that the generator's atomicity function."""
    files = [
        File("test.txt").from_content("File 1 content: {name}"),
        File("test2.txt").from_content("File 2 content: {name}"),
    ]
    generator.add_files(*files)
    generator.to_directory(tmp_path)
    generator.with_data({"name": "Michael"})

    (tmp_path / "test2.txt").write_text("I must not be overwritten")
    (tmp_path / "test2.txt").chmod(0o400)

    # Test non-atomicity first
    generator.overwrite(True)
    generator.atomic(False)

    with pytest.raises(FileCommitException):
        generator.execute()

    assert (tmp_path / "test.txt").exists()
    assert (tmp_path / "test2.txt").read_text() == "I must not be overwritten"

    # Test atomicity
    generator.atomic(True)

    with pytest.raises(FileCommitException):
        generator.execute()

    assert not (tmp_path / "test.txt").exists()
    assert (tmp_path / "test2.txt").read_text() == "I must not be overwritten"

    (tmp_path / "test2.txt").chmod(0o777)
