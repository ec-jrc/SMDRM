import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import geocode_tweets

import pandas
import pytest


# global places to test geocode
places_df = geocode_tweets.load_global_places()


@pytest.fixture()
def ambiguous_places():
    """Prefiltered Global Places test data with ambiguous city
    names i.e., homonym cities that exist in multiple Countries."""
    # filtering mask
    ambiguous_places_filter = places_df.city_name.isin(["Barcelona", "Alexandria"])
    yield places_df[ambiguous_places_filter].copy()
