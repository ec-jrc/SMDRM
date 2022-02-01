import pandas
import pytest
import requests
from tests.conftest import (
    transform_tweets,
    DeepPavlovMockResponse,
)



@pytest.fixture()
def datapoints_with_duplicates(datapoint_without_place, datapoint_with_gpe, datapoint_with_loc, datapoint_with_homonyms):
    """Datapoints with duplicates to test workaround to
    exclude duplicates from DeepPavlov tagging process."""
    yield pandas.DataFrame([
        datapoint_without_place,
        datapoint_with_gpe,
        datapoint_with_loc,
        # duplicate 1
        datapoint_with_gpe,
        # duplicate 2
        datapoint_with_gpe,
        datapoint_with_homonyms,
    ])


# deeppavlov output wrt to the datapoints_with_duplicates fixture
deeppavlov_output_payload = [
    [
        ["a", "text", "in", "english", "without", "place", "candidates", "."],
        ["Un", "texte", "d", "`", "information", "sur", "Rio", "de", "Janeiro", ",", "écrit", "à", "Paris", "."],
        ["ed", "uno", "in", "italiano", "da", "Roccacannuccia", "nella", "pianura", "pontina"],
        ['As', 'of', '6PM', 'Tuesday', ',', 'we', 'are', 'forecasting', 'flooding', 'at', 'the', 'following', 'locations', ':', 'Potomac', 'River', 'at', 'Alexandria', 'Potomac', 'River', 'at', 'Georgetown', '/', 'Wisconsin', 'Ave', 'Please', 'monitor', 'the', 'latest', 'forecasts', 'from', 'https', ':', '/', '/', 't', '.', 'co', '/', '47CQ6yEqJn', 'https', ':', '/', '/', 't', '.', 'co', '/', 'ODq4I1d0KN'],

        # adding duplicates
        ["Un", "texte", "d", "`", "information", "sur", "Rio", "de", "Janeiro", ",", "écrit", "à", "Paris", "."],
        ["Un", "texte", "d", "`", "information", "sur", "Rio", "de", "Janeiro", ",", "écrit", "à", "Paris", "."],
    ],
    [
        ["O", "O", "O", "B-LANGUAGE", "O", "O", "O", "O"],
        ["O", "O", "O", "O", "O", "O", "B-GPE", "I-GPE", "I-GPE", "O", "O", "O", "B-GPE", "O"],
        ["O", "B-CARDINAL", "O", "B-LANGUAGE", "O", "B-LOC", "I-LOC", "I-LOC", "I-LOC"],
        ['O', 'O', 'B-TIME', 'B-DATE', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O', 'B-GPE', 'B-LOC', 'I-LOC', 'O', 'B-GPE', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],

        # adding duplicates
        ["O", "O", "O", "O", "O", "O", "B-GPE", "I-GPE", "I-GPE", "O", "O", "O", "B-GPE", "O"],
        ["O", "O", "O", "O", "O", "O", "B-GPE", "I-GPE", "I-GPE", "O", "O", "O", "B-GPE", "O"],
    ],
]


def tag_with_mult_bert_mock(*args, **kwargs):
    """Mock function return our the mocked object with the .json() method."""
    return DeepPavlovMockResponse(payload=deeppavlov_output_payload)


def test_transform_datapoints(datapoints_with_duplicates, monkeypatch):
    """Test if transform datapoints execute the function
    calls correctly and excludes duplicates to be sent
    to DeepPavlov API for NER tagging."""

    # apply the monkeypatch to requests.post to mock tag_with_mult_bert()
    monkeypatch.setattr(requests, "post", tag_with_mult_bert_mock)

    datapoints_batches = iter([datapoints_with_duplicates])
    allowed_tags = ["B-GPE", "I-GPE", "etc...", ]

    # start transformation generator
    with pytest.raises(ValueError):
        # ValueError: Length of values (6) does not match length of index (4)

        # this raises a ValueError because transform_datapoints will send
        # only unique datapoints to tag_with_mult_bert()

        g = transform_tweets.transform_datapoints(datapoints_batches, allowed_tags)

        for _ in g:
            continue

