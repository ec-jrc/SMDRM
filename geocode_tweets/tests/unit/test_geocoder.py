import pytest
from tests.conftest import geocode_tweets


def test_load_global_places(ambiguous_places):
    """Test if load_global_places return the DataFrame with the expected fields."""
    expected_fields = [
        'city_id', 'city_name', 'city_asciiname', 'city_alternatenames',
        'latitude', 'longitude', 'population', 'country_code', 'country_name',
        'region_name', 'subregion_name', 'region_name_local', 'bbox',
        'region_id'
    ]
    assert list(ambiguous_places.columns) == expected_fields


def test_get_bbox_centroid():
    """Test if get_bbox_centroid returns the correct centroid latitude and longitude coords."""
    bbox = "13.762917,39.990139,15.807277,41.508354"
    expected_coords = (40.749246, 14.785097)
    result = geocode_tweets.get_bbox_centroid(bbox)
    assert result == expected_coords


def test_filter_places_by_bbox(ambiguous_places):
    """Test if filter_places_by_bbox obtains Alexandria with the bbox of Egypt."""
    egypt_bbox = dict(min_lon=28.965546, min_lat=30.262758, max_lon=30.108749, max_lat=31.359861)
    filtered_places = geocode_tweets.filter_places_by_bbox(ambiguous_places, **egypt_bbox)
    assert filtered_places.city_name.to_dict() == {6746: 'Alexandria'}, "There is only 1 Alexandria in Egypt."


def test_filter_places_by_region_id(ambiguous_places):
    """Test if filter_places_by_region returns the correct result given the region ID."""
    region_id = 633
    result = geocode_tweets.filter_places_by_region_id(region_id, ambiguous_places)
    assert (
        "Alexandria" in result.city_name.values
    ), "region_id {} should match the city of Alexandria (Egypt).".format(region_id)
    assert (
        "Egypt" in result.country_name.values
    ), "region_id {} should match the Country of Egypt.".format(region_id)


def test_filter_places_by_wrong_region_id(ambiguous_places):
    """Test if filter_places_by_region raises ValueError exception given the wrong region ID."""
    with pytest.raises(ValueError):
        geocode_tweets.filter_places_by_region_id(-1, ambiguous_places)


def test_get_gpes():
    """Test if get_gpes returns the expected gpes."""
    expected_gpes = ["a test", "place", "candidate"]
    datapoint = dict(place={"candidates": {"GPE": expected_gpes}})
    result = geocode_tweets.get_gpes(datapoint)
    assert result == expected_gpes


def test_get_gpes_with_min_len():
    """Test if get_gpes returns the expected gpes without `place` given the min_len threshold."""
    threshold = 6
    expected_gpes = ["a test", "place", "candidate"]
    datapoint = dict(place={"candidates": {"GPE": expected_gpes}})
    result = geocode_tweets.get_gpes(datapoint, min_len=threshold)
    assert result == ["a test", "candidate"]


def test_get_gpes_when_not_available():
    """Test if get_gpes returns an empty list if not available."""
    datapoint = dict(place={"candidates": None})
    result = geocode_tweets.get_gpes(datapoint)
    assert result == []


def test_flatten_gpes():
    """Test if flatten_gpes returns a list of strings
    if place candidates are made of multiple tokens."""
    multi_string_gpes = ["Friuli Venezia Giulia"]
    result = geocode_tweets.flatten_gpes(multi_string_gpes)
    assert result == ["Friuli", "Venezia", "Giulia"]


def test_get_city_filter(ambiguous_places):
    """Test if get_city_filter build a boolean mask
    wrt the given Global Places and GPEs."""
    result = geocode_tweets.get_city_filter(ambiguous_places, ["Barcelona"])
    assert result.sum() == 2
    countries = ambiguous_places[result].country_name.values
    assert "Spain" in countries and "Venezuela" in countries


def test_get_city_filter_with_unknown_gpe(ambiguous_places):
    """Test if get_city_filter returns an boolean mask of False for unknown GPE."""
    result = geocode_tweets.get_city_filter(ambiguous_places, ["unknown_gpe"])
    assert result.sum() == 0


def test_get_region_filter(ambiguous_places):
    """Test if get_region_filter build a boolean mask
    wrt the given Global Places and GPEs."""
    result = geocode_tweets.get_region_filter(ambiguous_places, ["Virginia"])
    assert result.sum() == 1
    assert "USA" in ambiguous_places[result].country_code.values

