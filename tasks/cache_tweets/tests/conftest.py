import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import cache_tweets

from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
import pytest


@pytest.fixture(scope="session")
def client():
    """Elasticsearch mocked client fixture."""
    mocked_client = mock.Mock(spec=Elasticsearch)
    return mocked_client("mock://client.py")


@pytest.fixture()
def datapoint():
    return {
        "id": 1219088193351495680,
        "created_at": "Mon Jan 20 02:44:09 +0000 2020",
        "lang": "es",
        "text": "RT @picks_goat: Excelente día en el Premium y pendiente una oficial y una FUN\n\nTeaser NFL POD 💰💰💰\n49ers TT over 27.5 💰💰💰\nBarcelona -2 XXX\nR…",
        "text_clean": "excelente día en el premium y pendiente una oficial y una fun teaser nfl pod 49ers tt over 275  2 xxx r _locincl_",
        "place": {
            "candidates": {"GPE": ["Barcelona"]},
            "meta": [
                {
                    "country_name": "Spain",
                    "country_code": "ESP",
                    "region_name": "Cataluña",
                    "city_name": "Barcelona",
                    "latitude": 41.38879,
                    "longitude": 2.15899,
                    "region_id": 9784,
                },
                {
                    "country_name": "Venezuela",
                    "country_code": "VEN",
                    "region_name": "Anzoátegui",
                    "city_name": "Barcelona",
                    "latitude": 10.13625,
                    "longitude": -64.68618,
                    "region_id": 2554,
                },
            ],
        },
        "annotation": {"floods": "0.040091"},
    }


@pytest.fixture()
def operations():
    return '{"index": {"_id": 1219088193351495680, "_index": "test_index"}}\n{"id": 1219088193351495680, "created_at": "Mon Jan 20 02:44:09 +0000 2020", "lang": "es", "text": "RT @picks_goat: Excelente d\\u00eda en el Premium y pendiente una oficial y una FUN\\n\\nTeaser NFL POD \\ud83d\\udcb0\\ud83d\\udcb0\\ud83d\\udcb0\\n49ers TT over 27.5 \\ud83d\\udcb0\\ud83d\\udcb0\\ud83d\\udcb0\\nBarcelona -2 XXX\\nR\\u2026", "text_clean": "excelente d\\u00eda en el premium y pendiente una oficial y una fun teaser nfl pod 49ers tt over 275  2 xxx r _locincl_", "place": {"candidates": {"GPE": ["Barcelona"]}, "meta": [{"country_name": "Spain", "country_code": "ESP", "region_name": "Catalu\\u00f1a", "city_name": "Barcelona", "latitude": 41.38879, "longitude": 2.15899, "region_id": 9784}, {"country_name": "Venezuela", "country_code": "VEN", "region_name": "Anzo\\u00e1tegui", "city_name": "Barcelona", "latitude": 10.13625, "longitude": -64.68618, "region_id": 2554}]}, "annotation": {"floods": "0.040091"}, "tags": ["test", "unit"]}\n'
