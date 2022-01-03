import pytest
from tests.conftest import extract_tweets


def test_extend_text_field(datapoint):
    result = extract_tweets.extend_text_field(datapoint)
    assert result == "a fake text"


def test_extend_text_field_with_missing_text():
    result = extract_tweets.extend_text_field(dict())
    assert result == ""


def test_parse_required_fields():
    pass


def test_parse_required_fields_non_legacy():
    pass


def test_parse_required_fields_with_invalid_json():
    pass


def test_make_ndjson_batches():
    pass
