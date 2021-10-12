"""
ElasticSearch Client and Index Templates
"""

import json
import typing

import requests

import libdrm.nicelogging
import libdrm.deploy


# ElasticSearch Index Templates for SMDRM Data Model
explicit_mapping = {
    "template": {
        "mappings": {
            "properties": {
                "annotation": {
                    "type": "float"
                },
                "created_at": {
                    "type": "date",
                    # Twitter date format
                    "format": "EEE LLL dd HH:mm:ss Z yyyy"
                },
                "id": {
                    "type": "text"
                },
                "img": {
                    "type": "object"
                },
                "lang": {
                    "type": "keyword"
                },
                "text": {
                    "type": "text"
                },
                "disaster_type": {
                    "type": "keyword"
                },
                "text_sanitized": {
                    "type": "text"
                },
                "uploaded_at": {
                    "type": "date",
                    # https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats
                    "format": "strict_date_optional_time"
                },
            }
        }
    }
}


def build_template(components: list):
    return {
        "index_patterns": ["smdrm-*", ],
        "template": {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 0
            },
            "mappings": {
                "_source": {
                    "enabled": True
                },
            },
        },
        "priority": 1,
        "composed_of": components,
        "version": 1,
        "_meta": {
            "description": "SMDRM Template composed of {}".format(components)
        }
    }


# console logging
console = libdrm.nicelogging.console_logger("elastic.client")


class ElasticSearchClient:
    """
    SMFR ElasticSearch Client to interact with the nodes.
    Usage:

    Create a reusable dynamic mapping component template and create an index pattern
        - es = ElasticSearchClient("http://localhost:9200", "smdrm-dev")
        - component_id = "dynamic_mapping"
        - es.build_component_template(component_id, dynamic_mapping)
        - es.create_index_template([component_id])
    Thereafter, any created index that matches the index patter will share the created template.
        - es.create_index()
    """

    def __init__(self, url: str, index: str):
        # format: http://host:port
        self.url = url
        self.index = index

    def __str__(self):
        return "ElasticSearchClient(url={})".format(self.url)

    def build_component_template(self, component_id, mapping):
        """
        There are two types of templates: index templates and component templates.
        Component templates are reusable building blocks that configure mappings,
        settings, and aliases. While you can use component templates to construct
        index templates, they aren’t directly applied to a set of indices. Index
        templates can contain a collection of component templates, as well as
        directly specify settings, mappings, and aliases.
        """
        response = requests.put(f"{self.url}/_component_template/{component_id}", json=mapping)
        console.debug(response.json())
        return response

    def create_index_template(self, component_ids: typing.List[str]) -> requests.Response:
        """
        An index template is a way to tell Elasticsearch how to configure an index when it is created.
        For data streams, the index template configures the stream’s backing indices as they are created.
        Templates are configured prior to index creation. When an index is created - either manually or through
        indexing a document - the template settings are used as a basis for creating the index.
        """
        console.info("Creating index template")
        response = requests.put(f"{self.url}/_index_template/smdrm_template", json=build_template(component_ids))
        console.debug(response.json())
        return response

    def create_index(self):
        self.build_component_template("explicit_mapping", explicit_mapping)
        self.create_index_template(["explicit_mapping"])
        response = requests.put(f"{self.url}/{self.index}")
        console.debug(response.json())
        return response

    def delete_index(self) -> requests.Response:
        response = requests.delete(f"{self.url}/{self.index}")
        console.debug(response.json())
        return response

    def doc_insert(self, data_point: dict) -> requests.Response:
        console.info("Add single data point to index")
        doc_id = data_point["id"]
        response = requests.post(f"{self.url}/{self.index}/_doc/{doc_id}", json=data_point)
        console.info("[{id}]: inserted".format(id=doc_id))
        console.debug(response.json())
        return response

    def bulk_insert(self, data_points: typing.List[dict]) -> requests.Response:
        console.info("Add multiple data points to index")
        ndjson_data = (
            "\n".join(
                "{meta}\n{event}".format(
                    meta=json.dumps({"create": {"_id": data_point["id"]}}),
                    event=json.dumps(data_point),
                )
                for data_point in data_points
            )
            + "\n"
        )
        response = requests.post(f"{self.url}/{self.index}/_bulk", headers={"Content-Type": "application/x-ndjson"}, data=ndjson_data)
        console.info("#{} documents inserted".format(len(data_points)))
        console.debug(response.json())
        return response
