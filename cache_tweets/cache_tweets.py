from datetime import datetime
import json
import logging
import os
import sys
import typing

from libdrm.datamodels import ZipFileModel
from libdrm.common import get_version, path_arg, log_execution

from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
from config import smdrm_component_template_config, smdrm_index_template_config

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("cache_tweets")


class ClientNotAvailable(Exception):
    pass


def build_index(index_suffix: str) -> str:
    """Build consistent index."""
    return "smdrm_" + index_suffix


def build_bulk_operations(
    index: str, datapoints: typing.List[dict], tags: typing.List[str] = None
) -> str:
    """Build bulk operations for datapoints batch in a single request.
    Source: https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html."""

    for datapoint in datapoints:
        # define operations on datapoint

        # add metadata
        meta = json.dumps({"index": {"_id": datapoint["id"], "_index": index}})
        # add tags
        event = json.dumps({**datapoint, **dict(tags=tags)})

        # bulk operation schema
        bulk_op = "{meta}\n{event}\n".format(meta=meta, event=event)

        yield bulk_op


def add_component_template(client: Elasticsearch, config: dict) -> ObjectApiResponse:
    """Put Elasticsearch component template into cluster."""
    return client.cluster.put_component_template(**config)


def add_index_template(client: Elasticsearch, config: dict) -> ObjectApiResponse:
    """Put Elasticsearch component template into cluster."""
    return client.indices.put_index_template(**config)


def create_index(client: Elasticsearch, index: str):
    """
    Create an Elasticsearch Index.
    Templates are applied to indices that match the index pattern in index_template.
    """
    return client.indices.create(index=index, wait_for_active_shards=1)


def index_exists(client: Elasticsearch, index: str) -> bool:
    """Check if index already exists."""
    return client.indices.exists(index=index).body


def cache_datapoints(client: Elasticsearch, operations: str) -> ObjectApiResponse:
    """
    Trigger a bulk_insert REST API requests with
    a list of operations for the given datapoint.
    """
    return client.bulk(operations=operations, source=True)


@log_execution(console)
def run(args):
    console.info("opts={}...".format(vars(args)))
    if args.debug:
        console.setLevel(logging.DEBUG)

    # input path validation
    zip_file = ZipFileModel(args.input_path)
    if not zip_file.is_valid():
        raise TypeError("Not a valid zip file.")

    # add filename as tag if no tags are given
    if not args.tags:
        console.warning("Input path appended to tags when --tags is None.")
        args.tags = [os.path.basename(args.input_path)]

    # build index
    index = build_index(args.index_suffix)

    # init client
    client = Elasticsearch(args.url)
    if not client.ping():
        raise ClientNotAvailable("ElasticSearch Client ping failed.")

    console.info("Put component template")
    add_component_template(client, smdrm_component_template_config)

    console.info("Put index template")
    add_index_template(client, smdrm_index_template_config)

    if not client.indices.exists(index=index).body:
        console.info("Create index {}".format(index))
        create_index(client, index)

    # cache data
    console.info("Cache datapoints to ElasticSearch")
    datapoints = zip_file.iter_jsonl()
    operations = build_bulk_operations(index, datapoints, tags=args.tags)
    bulk_response = cache_datapoints(client, operations)
    console.debug(bulk_response)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Caches enriched Twitter datapoints to ElasticSearch DB."
    )
    parser.add_argument(
        "--input-path",
        required=True,
        type=path_arg,
        help="Path from which you want to get input data.",
    )
    parser.add_argument(
        "--url",
        default="http://elasticsearch:9200",
        help="ElasticSearch url. Default is %(default)s.",
    )
    parser.add_argument(
        "--index-suffix",
        default=datetime.now().date().isoformat(),
        help="ElasticSearch index suffix. Default is %(default)s.",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        help="Additional tags to simplify ElasticSearch aggregations.",
    )
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
