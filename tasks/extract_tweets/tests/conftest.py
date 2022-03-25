import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import extract_tweets

import pytest


@pytest.fixture()
def valid_json_line():
    yield dict(
        id=1, created_at="datetime", lang="ml", text="a text from valid datapoint"
    )


@pytest.fixture()
def invalid_json_line():
    yield None


@pytest.fixture()
def preprocessed_json_line():
    yield {
        "unprocessed": dict(
            id=1, created_at="datetime", lang="ml", text="a text from legacy datapoint"
        ),
        "fake": "key",
    }


@pytest.fixture()
def json_lines(valid_json_line, invalid_json_line, preprocessed_json_line):
    yield iter([valid_json_line, invalid_json_line, preprocessed_json_line])
