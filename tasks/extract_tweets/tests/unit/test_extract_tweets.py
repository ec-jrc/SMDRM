import pytest
from tests.conftest import extract_tweets


def test_extend_text_field(valid_json_line):
    """Test if extend_text_field return the expected text string."""
    result = extract_tweets.extend_text_field(valid_json_line)
    assert result == "a text from valid datapoint"


def test_extend_text_field_with_missing_text(invalid_json_line):
    """Test if extend_text_field return an empty string for invalid json line."""
    result = extract_tweets.extend_text_field(invalid_json_line)
    assert result == ""


def test_filter_invalid_json_lines(json_lines):
    """Test if filter_invalid_json_lines discard the invalid json."""
    g = extract_tweets.filter_invalid_json_lines(json_lines)
    c = 0
    for _ in g:
        c += 1
    assert c == 2


def test_parse_raw_datapoints(preprocessed_json_line):
    """Test if parse_json_lines parsed the raw datapoint from a given field name"""
    g = extract_tweets.parse_json_lines(
        [preprocessed_json_line], field_id="unprocessed"
    )
    for res in g:
        assert res["text"] == "a text from legacy datapoint"


def test_build_datapoints(valid_json_line):
    """Test if build_datapoints returns the expected datapoint fields."""
    g = extract_tweets.build_datapoints([valid_json_line])
    for res in g:
        assert isinstance(res, dict)
        assert res == {
            "id": 1,
            "created_at": "datetime",
            "text": "a text from valid datapoint",
            "annotation": None,
            "text_clean": None,
            "place": None,
        }


def test_make_ndjson_batches(valid_json_line):
    """Test if make_ndjson_batches converts batch of dictionaries to batch of newline separated strings."""
    expected_batches = 2
    expected_datapoints_per_batch = 5

    g = extract_tweets.make_ndjson_batches([valid_json_line] * 10, batch_size=5)
    for batch_id, res in enumerate(g, start=1):
        continue

    # last batch_id from enumerate is the total number of batches
    assert expected_batches == batch_id
    # newline chars count to find the number of datapoints
    assert expected_datapoints_per_batch == res.count("\n")
