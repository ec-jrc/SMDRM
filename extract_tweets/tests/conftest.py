import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import extract_tweets

import pytest


@pytest.fixture()
def valid_datapoint():
    yield dict(id=1, created_at="datetime", lang="ml", text="a text from valid datapoint")


@pytest.fixture()
def invalid_datapoint():
    yield None


@pytest.fixture()
def processed_datapoint():
    yield {"unprocessed": dict(id=1, created_at="datetime", lang="ml", text="a text from legacy datapoint"), "fake": "key"}


@pytest.fixture()
def datapoints(valid_datapoint, invalid_datapoint, processed_datapoint):
    yield iter([valid_datapoint, invalid_datapoint, processed_datapoint])

