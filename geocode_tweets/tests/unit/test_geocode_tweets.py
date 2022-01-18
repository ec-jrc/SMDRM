import pytest
from tests.conftest import geocode_tweets


def test_filter_places_by_region_id(places_df):
    """Test if filter_places_by_region returns the correct result given the region ID."""
    region_id = 633
    result = geocode_tweets.filter_places_by_region_id(region_id, places_df)
    assert (
        "Alexandria" in result.city_name.values
    ), "region_id {} should match the city of Alexandria (Egypt).".format(region_id)
    assert (
        "Egypt" in result.country_name.values
    ), "region_id {} should match the Country of Egypt.".format(region_id)


def test_filter_places_by_wrong_region_id(places_df):
    """Test if filter_places_by_region raises ValueError exception given the wrong region ID."""
    with pytest.raises(ValueError):
        geocode_tweets.filter_places_by_region_id(-1, places_df)


def test_make_place_reference_key(places_df):
    """Test if make_place_reference_key concatenates the place names correctly."""
    alexandria_egypt_index = 6746
    result = geocode_tweets.make_place_reference_key(places_df)
    ref_key = result[alexandria_egypt_index]
    assert len(ref_key) == 295
    assert (
        ref_key
        == "Alexandria,Alexandria,ALY,Al Iskandariyah,Al Iskandarīyah,Alegsandiri,Alegsàndiri,Alehandriya,Aleixandria,Aleixandría,Alejandria,Alejandría,Aleksandria,Aleksandrii,Aleksandrij,Aleksandrija,Aleksandrio,Aleksandriya,Aleksandrje,Aleksandryja,Aleksandryjo,Alesandria dEgito,Al,Egypt,Al Iskandariyah,"
    )


def test_make_place_candidate_match_mask_with_country_gpe(places_df):
    """Test if make_place_candidate_match_mask creates the
    correct matches mask given a GPE Country place candidate."""
    refkey = geocode_tweets.make_place_reference_key(places_df)
    # create masks and count matches wrt the GPE place candidate given
    # mask.sum() counts matches (True occurrences)
    test_country_mask = geocode_tweets.make_place_candidate_match_mask(
        "romania", refkey
    )
    assert test_country_mask.sum() == 1, "There is only 1 Alexandria City in Romania."


def test_make_place_candidate_match_mask_with_city_gpe(places_df):
    """Test if make_place_candidate_match_mask creates the
    correct matches mask given a GPE City place candidate."""
    refkey = geocode_tweets.make_place_reference_key(places_df)
    # create masks and count matches wrt the GPE place candidate given
    # mask.sum() counts matches (True occurrences)
    test_city_mask = geocode_tweets.make_place_candidate_match_mask("barcelona", refkey)
    assert (
        test_city_mask.sum() == 2
    ), "There are 2 Barcelona cities in Global Places: Spain, and Venezuela."


def test_make_place_candidate_match_mask_with_unknown_gpe(places_df):
    """Test if make_place_candidate_match_mask creates the
    correct matches mask given a unknown GPE place candidate."""
    refkey = geocode_tweets.make_place_reference_key(places_df)
    # create masks and count matches wrt the GPE place candidate given
    # mask.sum() counts matches (True occurrences)
    test_unknown_gpe_mask = geocode_tweets.make_place_candidate_match_mask(
        "unknown_gpe", refkey
    )
    assert (
        test_unknown_gpe_mask.sum() == 0
    ), "The `unknown_gpe` GPE does not exist in Global Places."


def test_make_place_candidate_match_mask_with_gpe_substring(places_df):
    """Test if make_place_candidate_match_mask creates the
    correct matches mask given a GPE substring place candidate."""
    refkey = geocode_tweets.make_place_reference_key(places_df)
    # create masks and count matches wrt the GPE place candidate given
    # mask.sum() counts matches (True occurrences)
    test_substring_gpe_mask = geocode_tweets.make_place_candidate_match_mask(
        "Alexandria United States", refkey
    )
    # there should be 2 US states with Alexandria city, namely Louisiana, and Virginia
    # however, the given gpe matches alexandria keyword in Egypt and Romania too due to
    # the OR logical operator pattern in make_place_reference_key
    assert test_substring_gpe_mask.sum() == 4
    # this issue is resolved if we filter the Global Places using the region_id
    us_virginia_region_id = 12926
    filtered_places_df = geocode_tweets.filter_places_by_region_id(
        us_virginia_region_id, places_df
    )
    filtered_refkey = geocode_tweets.make_place_reference_key(filtered_places_df)
    test_substring_gpe_mask_filtered = geocode_tweets.make_place_candidate_match_mask(
        "Alexandria United States", filtered_refkey
    )
    assert (
        test_substring_gpe_mask_filtered.sum() == 1
    ), "There is only 1 Alexandria City in the state of Virginia US."


def test_get_bbox_centroid():
    """Test if get_bbox_centroid returns the correct centroid latitude and longitude coords."""
    bbox = "13.762917,39.990139,15.807277,41.508354"
    expected_coords = (40.7492465, 14.785097)
    result = geocode_tweets.get_bbox_centroid(bbox)
    assert result == expected_coords


def test_geocode_with_single_matching_gpe(places_df):
    """Test if geocode return the geocode metadata at
    city level as the given gpe produces only one match."""
    gpes = ["Alexandria Potomac River"]
    us_virginia_region_id = 12926
    filtered_places_df = geocode_tweets.filter_places_by_region_id(us_virginia_region_id, places_df)
    result = geocode_tweets.geocode(gpes, us_virginia_region_id, filtered_places_df)
    expected = {'region_id': 12926, 'latitude': 38.80484, 'longitude': -77.04692, 'name': 'Alexandria', 'type': 'city'}
    assert result == expected


def test_geocode_with_short_gpe(places_df):
    """Test if geocode return None as the given gpe
    length is shorter than the condition (3 chars)."""
    gpes = ["US"]
    us_virginia_region_id = 12926
    filtered_places_df = geocode_tweets.filter_places_by_region_id(us_virginia_region_id, places_df)
    result = geocode_tweets.geocode(gpes, us_virginia_region_id, filtered_places_df)
    assert not result

