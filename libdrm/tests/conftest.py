import json
import pathlib
import pytest
import zipfile


# set the current directory from __file__
this_path = pathlib.Path(__file__).resolve().parent


@pytest.fixture()
def valid_json():
    return dict(
        id=123456789,
        created_at="Sat May 15 08:49:13 +0000 2021",
        text="A text to be annotated with floods model",
        lang="it",
        disaster_type="floods",
    )


@pytest.fixture()
def invalid_json():
    return dict(
        id=123,
        disaster_type="unknown",
    )


@pytest.fixture()
def valid_bytes(valid_json):
    return json.dumps(valid_json).encode("utf-8")


@pytest.fixture()
def invalid_bytes(invalid_json):
    return json.dumps(invalid_json).encode("utf-8")


@pytest.fixture()
def valid_zipfile(valid_bytes):
    """
    Test a bad zip file created on the fly.
    """
    tmp_zipfile = this_path / "valid.zip"
    with zipfile.ZipFile(tmp_zipfile, "w") as zip_file:
        zip_file.writestr("valid.json", valid_bytes)
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def invalid_zipfile():
    """
    Test a bad zip file created on the fly.
    """
    tmp_zipfile = this_path / "invalid.zip"
    with open(tmp_zipfile, "w") as not_zip_file:
        not_zip_file.write("whatever")
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()
