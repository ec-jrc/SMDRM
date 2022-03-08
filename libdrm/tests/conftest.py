import pytest
import os

# directory of this file
cwd = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def valid_archive_path():
    """Path to valid zip file data."""
    return os.path.join(cwd, "data/valid.zip")


@pytest.fixture()
def invalid_archive_path():
    """Path to invalid zip file data."""
    return os.path.join(cwd, "data/invalid.zip")


@pytest.fixture()
def wrong_archive_path():
    """Path to wrong zip file data."""
    return os.path.join(cwd, "data/wrong.zip")

