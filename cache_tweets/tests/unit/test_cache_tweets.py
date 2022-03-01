from datetime import datetime
import pytest
import typing
from conftest import cache_tweets



def test_build_index():
    """Test build_index()."""

    assert cache_tweets.build_index("custom_suffix") == "smdrm_custom_suffix"


def test_add_component_template(client):
    """Test add_component_template() calls the correct resources with the expected arguments."""

    actual = cache_tweets.add_component_template(client, dict(component="template"))
    client.cluster.put_component_template.assert_called_once_with(component="template")


def test_add_index_template(client):
    """Test add_index_template() calls the correct resources with the expected arguments."""

    actual = cache_tweets.add_index_template(client, dict(index="template", settings={"shards": 1}))
    client.indices.put_index_template.assert_called_once_with(index="template", settings={"shards": 1})


def test_create_index(client):
    """Test create_index() calls the correct resources with the expected arguments."""

    actual = cache_tweets.create_index(client, index="test_index")
    client.indices.create.assert_called_once_with(index="test_index", wait_for_active_shards=1)


def test_index_exists(client):
    """Test index_exists() calls the correct resources with the expected arguments."""

    actual = cache_tweets.index_exists(client, index="test_index")
    client.indices.exists.assert_called_once_with(index="test_index")


def test_build_bulk_operations(datapoint, operations):
    """
    Test if cache_tweets.build_bulk_operations() creates ElasticSearch bulk operations
    to cache NDJSON datapoints to the ElasticSearch index.
    """

    index = "test_index"
    tags = ["test", "unit"]
    datapoints = [datapoint,]

    # operations
    actual = cache_tweets.build_bulk_operations(index, datapoints, tags)
    assert isinstance(actual, typing.Generator)
    assert next(actual) == operations


def test_cache_datapoints(client, operations):
    """Test cache_datapoints() with valid operations."""

    actual = cache_tweets.cache_datapoints(client, operations)
    client.bulk.assert_called_once_with(operations=operations, source=True)

