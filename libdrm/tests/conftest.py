import pytest
import os

this_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def valid_archive_path():
    """Path to valid zip file data."""
    return os.path.join(this_dir, "data/valid.zip")


@pytest.fixture()
def invalid_archive_path():
    """Path to invalid zip file data."""
    return os.path.join(this_dir, "data/invalid.zip")


@pytest.fixture()
def wrong_archive_path():
    """Path to wrong zip file data."""
    return os.path.join(this_dir, "data/wrong.zip")


@pytest.fixture()
def valid_raw_input():
    """A valid JSON format bytes string not converted."""
    return b'{"id": "1", "created_at": "date", "lang": "id", "text": "text"}'


@pytest.fixture()
def invalid_raw_input():
    """A invalid JSON format bytes string."""
    return b'Does it look valid JSON bytes to you??'


@pytest.fixture()
def enriched_input():
    """`enriched_input` is the `valid_raw_input` that passed convert step.
    DataPointModel expects a filename as required field."""
    return b'{"id": "1", "created_at": "date", "lang": "id", "text": "text", "filename": "/data/file.zip"}'
