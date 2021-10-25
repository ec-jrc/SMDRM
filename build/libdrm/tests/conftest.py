import json
import pathlib
import pytest
import zipfile
import libdrm.pipeline


# set the current directory from __file__
this_path = pathlib.Path(__file__).resolve().parent


@pytest.fixture()
def valid_json():
    """An valid data point."""
    return dict(
        id="123456789",
        created_at="Sat May 15 08:49:13 +0000 2021",
        text="A text to be annotated with floods model",
        lang="it",
    )


@pytest.fixture()
def invalid_json():
    """An invalid data point."""
    return dict(
        unknown_key="unknown_value",
    )


@pytest.fixture()
def valid_bytes(valid_json):
    """Converts dict to bytes."""
    return json.dumps(valid_json).encode("utf-8")


@pytest.fixture()
def invalid_bytes(invalid_json):
    """Converts dict to bytes."""
    return json.dumps(invalid_json).encode("utf-8")


@pytest.fixture()
def valid_metadata():
    """Fixture that returns synthetic metadata from user requests.
    This fixture must be updated when more APIs become available.
    For more info, check the `APIs_lookup` dictionary in libdrm.apis."""
    return {"floods_annotator": True, "tags": "test-tag1,test-tag2"}


@pytest.fixture()
def invalid_metadata():
    return {"floods_annotator": "invalid value"}


@pytest.fixture()
def valid_zipfile(valid_bytes):
    """Fixture that creates a zip file at runtime with valid JSON bytes."""
    tmp_zipfile = this_path / "valid.zip"
    with zipfile.ZipFile(tmp_zipfile, "w") as zip_file:
        zip_file.writestr("valid.json", valid_bytes)
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def invalid_zipfile():
    """Fixture that creates an invalid zip file at runtime."""
    tmp_zipfile = this_path / "invalid.zip"
    with open(tmp_zipfile, "w") as zip_file:
        zip_file.write("valid.json")
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def valid_zipfile_invalid_json():
    """Fixture that creates a zip file at runtime with invalid JSON bytes."""
    tmp_zipfile = this_path / "valid.zip"
    with zipfile.ZipFile(tmp_zipfile, "w") as zip_file:
        zip_file.writestr("invalid.json", b"this is not JSON!")
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def valid_json_files_iterator(valid_zipfile):
    """Fixture that standardizes ZipFilesToJSONFiles pipeline step,
    and returns valid JSON files."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    yield step.logic([valid_zipfile])


@pytest.fixture()
def invalid_json_files_iterator(valid_zipfile_invalid_json):
    """Fixture that standardizes ZipFilesToJSONFiles pipeline step,
    and returns invalid JSON files."""
    step = libdrm.pipeline.ZipFilesToJSONFiles()
    yield step.logic([valid_zipfile_invalid_json])


@pytest.fixture()
def valid_json_bytes_iterator(valid_zipfile):
    """Fixture that build a Pipeline Class with ZipFilesToJSONFiles,
    and JSONFilesToJSONLines steps to returns batches of valid JSON bytes."""
    steps = [
        libdrm.pipeline.ZipFilesToJSONFiles(),
        libdrm.pipeline.JSONFilesToJSONLines()
    ]
    # create 25 copies of valid zipfile
    pipeline = libdrm.pipeline.Pipeline([valid_zipfile]*25, steps)
    yield pipeline.build()
