import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import annotate_tweets

import pytest


@pytest.fixture()
def datapoint():
    yield dict(text="a fake text")


@pytest.fixture()
def datapoints():
    yield [
        dict(),
    ]
