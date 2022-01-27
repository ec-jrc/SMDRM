import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import geocode_tweets
import pandas
import pytest


@pytest.fixture()
def datapoint_without_place():
    """Datapoint without place."""
    yield {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "es",
        "text": "Los pasajes más bonitos de Barcelona https://t.co/vycifpLVWy",
        "annotation": {
            "floods": "0.1"
            },
        "text_clean": "los pasajes más bonitos de    _urlincl_ _locincl_",
        "place": None,
    }


@pytest.fixture()
def datapoint_with_gpe():
    """Datapoint with place."""
    yield {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "es",
        "text": "Los pasajes más bonitos de Barcelona https://t.co/vycifpLVWy",
        "annotation": {
            "floods": "0.1"
            },
        "text_clean": "los pasajes más bonitos de    _urlincl_ _locincl_",
        "place": {
            "candidates": {
                "GPE": ["Barcelona"],
            }
        },
    }


@pytest.fixture()
def datapoint_with_ambiguous_gpe():
    """Datapoint with homonym places i.e. Alexandria (Egypt, US)."""
    yield {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "es",
        "text": "As of 6PM Tuesday, we are forecasting flooding at the following locations: Potomac River at Alexandria Potomac River at Georgetown/Wisconsin Ave Please monitor the latest forecasts from https://t.co/47CQ6yEqJn https://t.co/ODq4I1d0KN",
        "annotation": {
            "floods": "0.1"
            },
        "text_clean": "as of tuesday we are forecasting flooding at the following locations  at alexandria  at wisconsin ave please monitor the latest forecasts from    _urlincl_ _locincl_",
        "place": {
            "candidates": {
                "LOC": ["Potomac River", "Potomac River"],
                "GPE": ["Alexandria Potomac River", "Georgetown"],
            },
        },
    }


@pytest.fixture()
def datapoints():
    yield [datapoint_without_place, datapoint_with_gpe, datapoint_with_ambiguous_gpe]


@pytest.fixture()
def places_df():
    """Prefiltered Global Places test data with ambiguous city
    names i.e., homonym cities that exist in multiple Countries."""
    # global places to test geocode
    df = geocode_tweets.load_global_places()
    # filtering mask
    ambiguous_gpes_mask = df.city_name.isin(["Barcelona", "Alexandria"])
    # fillna remove NaN values in all fields
    # NaN values transform all attributes in NaN
    yield df[ambiguous_gpes_mask].copy(deep=True).fillna("")

