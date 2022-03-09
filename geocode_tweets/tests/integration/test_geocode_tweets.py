from tests.conftest import geocode_tweets


def test_geocode_datapoints_with_cities(ambiguous_places):
    """Test if geocode_datapoints returns
    the enriched version of a given datapoint."""

    datapoint = {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "en",
        "text": "As of 6PM Tuesday, we are forecasting flooding at the following locations: Potomac River at Alexandria Potomac River at Georgetown/Wisconsin Ave Please monitor the latest forecasts from https://t.co/47CQ6yEqJn https://t.co/ODq4I1d0KN",
        "text_clean": "as of tuesday we are forecasting flooding at the following locations  at alexandria  at wisconsin ave please monitor the latest forecasts from    _urlincl_ _locincl_",
        "place": {
            "candidates": {
                "LOC": ["Potomac River", "Potomac River"],
                "GPE": ["Alexandria Potomac River", "Georgetown"],
            }
        },
    }

    geocoded = {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "en",
        "text": "As of 6PM Tuesday, we are forecasting flooding at the following locations: Potomac River at Alexandria Potomac River at Georgetown/Wisconsin Ave Please monitor the latest forecasts from https://t.co/47CQ6yEqJn https://t.co/ODq4I1d0KN",
        "text_clean": "as of tuesday we are forecasting flooding at the following locations  at alexandria  at wisconsin ave please monitor the latest forecasts from    _urlincl_ _locincl_",
        "place": {
            "candidates": {
                "LOC": ["Potomac River", "Potomac River"],
                "GPE": ["Alexandria Potomac River", "Georgetown"],
            },
            "meta": [
                {
                    "country_name": "Romania",
                    "country_code": "ROU",
                    "region_name": "Teleorman",
                    "city_name": "Alexandria",
                    "region_id": 1865,
                    "latitude": 43.98333,
                    "longitude": 25.33333,
                },
                {
                    "country_name": "United States",
                    "country_code": "USA",
                    "region_name": "Virginia",
                    "city_name": "Alexandria",
                    "region_id": 12926,
                    "latitude": 38.80484,
                    "longitude": -77.04692,
                },
            ],
        },
    }

    datapoints = iter([datapoint])
    result = next(geocode_tweets.geocode_datapoints(datapoints, ambiguous_places))
    assert result == geocoded


def test_geocode_datapoints_with_regions(ambiguous_places):
    """Test if geocode_datapoints returns multiple places in the enriched datapoint."""

    datapoint = {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "en",
        "text": "Code red in multiple US states: Louisiana, Virginia are hit the most. Info at https://t.co/whatever",
        "text_clean": "not needed...",
        "place": {
            "candidates": {
                "GPE": ["Louisiana", "Virginia", "US"],
            }
        },
    }

    geocoded = {
        "id": 1219088163542532096,
        "created_at": "Mon Jan 20 02:44:02 +0000 2020",
        "lang": "en",
        "text": "Code red in multiple US states: Louisiana, Virginia are hit the most. Info at https://t.co/whatever",
        "text_clean": "not needed...",
        "place": {
            "candidates": {"GPE": ["Louisiana", "Virginia", "US"]},
            "meta": [
                {
                    "country_name": "United States",
                    "country_code": "USA",
                    "region_name": "Louisiana",
                    "region_id": 11258,
                    "latitude": 31.204971,
                    "longitude": -92.527046,
                },
                {
                    "country_name": "United States",
                    "country_code": "USA",
                    "region_name": "Virginia",
                    "region_id": 12926,
                    "latitude": 38.817146,
                    "longitude": -77.091072,
                },
            ],
        },
    }

    datapoints = iter([datapoint])
    result = next(geocode_tweets.geocode_datapoints(datapoints, ambiguous_places))
    assert result == geocoded
