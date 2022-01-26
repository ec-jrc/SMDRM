import pytest
from tests.conftest import extract_tweets


def test_extend_text_field(valid_datapoint):
    """Test if extend_text_field return the expected text string."""
    result = extract_tweets.extend_text_field(valid_datapoint)
    assert result == "a text from valid datapoint"


def test_extend_text_field_with_missing_text(invalid_datapoint):
    """Test if extend_text_field return an empty string for invalid datapoints."""
    result = extract_tweets.extend_text_field(invalid_datapoint)
    assert result == ""


def test_filter_invalid_datapoints(datapoints):
    """Test if filter_invalid_datapoints discard the invalid datapoint in datapoints fixture."""
    g = extract_tweets.filter_invalid_datapoints(datapoints)
    c = 0
    for _ in g:
        c += 1
    assert c == 2


def test_parse_raw_datapoints(processed_datapoint):
    """Test if parse_raw_datapoints parsed the raw datapoint from a given field name"""
    datapoints = [processed_datapoint]
    g = extract_tweets.parse_raw_datapoints(datapoints, raw_datapoint_field="unprocessed")
    for res in g:
        assert res['text'] == 'a text from legacy datapoint'


def test_build_datamodel(valid_datapoint):
    """Test if build_datamodel returns the expected datamodel structure."""
    datapoints = [valid_datapoint]
    g = extract_tweets.build_datamodel(datapoints)
    for res in g:
        assert isinstance(res, dict)
        assert res == {'id': 1, 'created_at': 'datetime', 'lang': 'ml', 'text': 'a text from valid datapoint', 'text_clean': None, 'places': None}


def test_make_ndjson_batches(valid_datapoint):
    """Test if make_ndjson_batches converts batch of dictionaries to batch of newline separated strings."""
    datapoints = [valid_datapoint]*10
    expected_batches = 2
    expected_datapoints_per_batch = 5

    g = extract_tweets.make_ndjson_batches(datapoints, batch_size=5)
    for batch_id, res in enumerate(g, start=1):
        continue

    # last batch_id from enumerate is the total number of batches
    assert expected_batches == batch_id
    # newline chars count to find the number of datapoints
    assert expected_datapoints_per_batch == res.count("\n")

