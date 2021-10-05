import json
import pathlib
import zipfile

import pytest
import sys

this_path = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(this_path.parent))
from src import pipelines


@pytest.fixture()
def valid_json():
    return {
        "created_at": "Sat May 15 14:25:35 +0000 2021",
        "id": "1",
        "text": "A text information.",
        "lang": "en",
        "disaster_type": "floods",
    }


@pytest.fixture()
def valid_json_bytes(valid_json):
    return json.dumps(valid_json).encode("utf-8")


@pytest.fixture()
def invalid_json_bytes():
    return b"this is not JSON!"


@pytest.fixture()
def valid_zipfile(valid_json_bytes):
    """
    Test a bad zip file created on the fly.
    """
    tmp_zipfile = this_path / "valid.zip"
    with zipfile.ZipFile(tmp_zipfile, "w") as zip_file:
        zip_file.writestr("valid.json", valid_json_bytes)
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def invalid_zipfile():
    """
    Test a bad zip file created on the fly.
    """
    tmp_zipfile = this_path / "invalid.zip"
    with open(tmp_zipfile, "w") as zip_file:
        zip_file.write("valid.json")
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def valid_zipfile_invalid_json(invalid_json_bytes):
    """
    Test a bad zip file created on the fly.
    """
    tmp_zipfile = this_path / "valid.zip"
    with zipfile.ZipFile(tmp_zipfile, "w") as zip_file:
        zip_file.writestr("invalid.json", invalid_json_bytes)
    yield tmp_zipfile
    # remove tmp file
    tmp_zipfile.unlink()


@pytest.fixture()
def zip_files(valid_zipfile, invalid_zipfile):
    return [valid_zipfile, invalid_zipfile]
