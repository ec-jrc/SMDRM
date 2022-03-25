import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import transform_tweets
import transformations

import pytest


# datapoint without place candidates
@pytest.fixture()
def datapoint_without_place():
    yield {
        "id": 1,
        "created_at": "datetime",
        "lang": "en",
        "text": "a text in english without place candidates.",
        "annotation": None,
        "text_clean": None,
        "place": None,
    }


# datapoint with GPE place candidates
@pytest.fixture()
def datapoint_with_gpe():
    yield {
        "id": 2,
        "created_at": "datetime",
        "lang": "fr",
        "text": "Un texte d`information sur Rio de Janeiro, écrit à Paris.",
        "annotation": None,
        "text_clean": None,
        "place": None,
    }


# datapoint with LOC place candidates
@pytest.fixture()
def datapoint_with_loc():
    yield {
        "id": 3,
        "created_at": "datetime",
        "lang": "it",
        "text": "ed uno in italiano da Roccacannuccia nella pianura pontina",
        "annotation": None,
        "text_clean": None,
        "place": None,
    }


# Datapoint with homonym places i.e. Alexandria (Egypt, US)
@pytest.fixture()
def datapoint_with_homonyms():
    yield {
        "id": 4,
        "created_at": "datetime",
        "lang": "en",
        "text": "As of 6PM Tuesday, we are forecasting flooding at the following locations: Potomac River at Alexandria Potomac River at Georgetown/Wisconsin Ave Please monitor the latest forecasts from https://t.co/47CQ6yEqJn https://t.co/ODq4I1d0KN",
        "annotation": None,
        "text_clean": None,
        "place": None,
    }


@pytest.fixture()
def allowed_tags():
    yield ["B-GPE", "I-GPE", "B-FAC", "I-FAC", "B-LOC", "I-LOC"]


class DeepPavlovMockResponse:
    """Custom class to mock the return value of tag_with_mult_bert()
    will override the requests.Response returned from requests.post"""

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        """mock json() method always returns a specific testing dictionary
        you can override this value when needed."""
        return self.payload
