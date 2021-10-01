# -*- coding: utf-8 -*-

"""
ElasticSearch Client and index templates

Add events to Elasticsearch:

  * payload = {'username': 'bob', 'email': 'bob@bob.com'}
  * request = requests.put("http://localhost:9200/index_id/_doc/tweet_id", data=payload)

"""

import json
import sys
import requests
import time

from libdrm.nicelogging import setup_logger


logger = setup_logger("smdrm.elastic.client")


template = {
    "settings": {"index": {"number_of_shards": "1", "number_of_replicas": "0"}},
    "mappings": {
        "dynamic_date_formats": [
            "strict_date_optional_time",
            "EEE MMM dd HH:mm:ss Z YYYY",   # Twitter date format
        ],
        "properties": {
            "annotations": {"type": "object"},
            "annotations.floods": {"type": "float"},
            "annotations.fires": {"type": "float"},
            "created_at": {"type": "date", "format": "EEE LLL dd HH:mm:ss Z yyyy"},
            "id": {"type": "text"},
            "img": {"type": "object"},
            "lang": {"type": "keyword"},
            "text": {"type": "text"},
            "disaster_type": {"type": "keyword"},
            "text_sanitized": {"type": "text"},
            "uploaded_at": {"type": "date", "format": "strict_date_optional_time"},
        },
    },
}

# dynamic_mappings = {
#     "mappings": {
#         "dynamic_date_formats": [
#             "strict_date_optional_time",
#             "EEE MMM dd HH:mm:ss Z YYYY",
#         ],
#         "dynamic_templates": [
#             {"strings_as_keywords": {"match_mapping_type": "string", "runtime": {}}}
#         ],
#     }
# }


class ElasticSearchClient:
    """
    SMFR ElasticSearch Client to interact with the nodes.
    """

    def __init__(self, host: str = "localhost", port: int = 9200, index: str = "smdrm-dev"):
        self.host = host
        self.port = port
        # TODO: add yearly freq
        self.index = index

    @property
    def url(self) -> str:
        return "http://{host}:{port}/{index}".format(host=self.host, port=self.port, index=self.index)

    def ping(self) -> requests.Response:
        try:
            return requests.get(self.url.replace(self.index, ""))
        except requests.exceptions.ConnectionError:
            response = requests.Response()
            response.status_code = 400
            return response

    def wait_for_it(self, seconds: int = 10, max_attempts: int = 5) -> None:
        ready = False
        attempts = 0
        while not ready:
            attempts += 1
            response = self.ping()
            logger.info("Ping ElasticSearch API: attempt {}/{} - next in {}".format(attempts, max_attempts, seconds))
            if response.status_code != 200:
                time.sleep(seconds)
                if attempts == max_attempts:
                    logger.info("max attempts reached. exiting...")
                    sys.exit(35)
                continue
            ready = True
        logger.info("ElasticSearch API is ready!")

    def create_index(self, index_template: dict = None) -> requests.Response:
        response = requests.get(self.url)
        if response.status_code != 200:
            response = requests.put(self.url, json=template or index_template)
            logger.info("Index created")
        logger.debug("Index metadata: {}".format(response.json()))
        return response

    def delete_index(self) -> requests.Response:
        response = requests.delete(self.url)
        logger.info("Index deleted")
        logger.debug(response.json())
        return response

    def doc_insert(self, data_point: dict) -> requests.Response:
        # add single event to index
        doc_id = data_point['id']
        response = requests.post(f"{self.url}/_doc/{doc_id}", json=data_point)
        logger.info("[{id}]: inserted".format(id=doc_id))
        logger.debug(response.json())
        return response

    def bulk_insert(self, data_points: dict) -> requests.Response:
        # add multiple events to index
        ndjson_data = (
            "\n".join(
                "{meta}\n{event}".format(
                    meta=json.dumps({"create": {"_id": _id}}),
                    event=json.dumps(data_point),
                )
                for _id, data_point in data_points.items()
            )
            + "\n"
        )
        response = requests.post(
            f"{self.url}/_bulk",
            headers={"Content-Type": "application/x-ndjson"},
            data=ndjson_data,
        )
        logger.info("bulk documents inserted")
        logger.debug(response.json())
        return response
