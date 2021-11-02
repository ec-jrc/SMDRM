"""
ElasticSearch Client and Index Templates
"""

import datetime
import json
import typing
import requests


# ElasticSearch Index Templates for SMDRM Data Model
explicit_component_template = {
    "template": {
        "mappings": {
            "properties": {
                "annotations": {
                    "type": "nested",
                    "include_in_parent": True,
                    "properties": {
                        "annotation_type": {
                           "type": "keyword"
                        },
                        "annotation_prob": {
                            "type": "float"
                        },
                        "sanitized_text": {
                            "type": "text"
                        }
                    }
                },
                "created_at": {
                    "type": "date",
                    # Twitter date format
                    "format": "EEE LLL dd HH:mm:ss Z yyyy"
                },
                "id": {
                    "type": "text"
                },
                "lang": {
                    "type": "keyword"
                },
                "text": {
                    "type": "text"
                },
                "latitude": {
                    "type": "float"
                },
                "longitude": {
                    "type": "float"
                },
                "place_name": {
                    "type": "keyword"
                },
                "place_type": {
                    "type": "keyword"
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


class ElasticSearchClient:
    """
    SMFR ElasticSearch Client to interact with the nodes.
    Usage:

    Initialize the ElasticSearch client:
      es = ElasticSearchClient("http://localhost:9200")
    The __init__() method sets the index, component and the index templates used at index creation.
      es.index
      es._component_id
      es._component_template
      es._index_template
    You can create the ElasticSearch index:
      es.create_index()
    The create_index() method will create a reusable component template and index template
    Now, any created index that matches the index patter will share the created template.
    """

    def __init__(self, url: str, index_prefix: str = "smdrm", component_id: str = None, component_template: dict = None, shards: int = 3, replicas: int = 0):
        # format: http://host:port
        self.url = url
        # index id
        self.index = "{prefix}_{date}".format(prefix=index_prefix, date=datetime.datetime.today().date().isoformat())
        # component template
        self._component_id = component_id or "explicit_component_template"
        self._component_template = component_template or explicit_component_template
        # index template
        self._index_template = {
            "index_patterns": ["{}_*".format(index_prefix), ],
            "template": {
                "settings": {
                    "number_of_shards": shards,
                    "number_of_replicas": replicas,
                },
                "mappings": {
                    "_source": {
                        "enabled": True
                    },
                },
            },
            "priority": 1,
            "composed_of": [self._component_id],
            "version": 1,
        }

    def __str__(self):
        return "ElasticSearchClient(url={url}, index={index})".format(url=self.url, index=self.index)

    def build_component_template(self, component_id, component_mapping):
        """
        There are two types of templates: index templates and component templates.
        Component templates are reusable building blocks that configure mappings,
        settings, and aliases. While you can use component templates to construct
        index templates, they are not directly applied to a set of indices. Index
        templates can contain a collection of component templates, as well as
        directly specify settings, mappings, and aliases.
        """
        return requests.put(
            "{url}/_component_template/{cid}".format(url=self.url, cid=component_id),
            json=component_mapping
        )

    def create_index_template(self, index_template) -> requests.Response:
        """
        An index template is a way to tell Elasticsearch how to configure an index when it is created.
        For data streams, the index template configures the stream’s backing indices as they are created.
        Templates are configured prior to index creation. When an index is created - either manually or through
        indexing a document - the template settings are used as a basis for creating the index.
        """
        return requests.put(
            "{url}/_index_template/{index}_template".format(url=self.url, index=self.index),
            json=index_template
        )

    def create_index(self) -> requests.Response:
        """Create the index."""
        self.build_component_template(self._component_id, self._component_template)
        self.create_index_template(self._index_template)
        return requests.put("{url}/{index}".format(url=self.url, index=self.index))

    def delete_index(self) -> requests.Response:
        """Delete the index."""
        return requests.delete("{url}/{index}".format(url=self.url, index=self.index))

    def doc_insert(self, data_point: dict) -> requests.Response:
        """Execute a doc insert operation to process an event in a single request.
        The document attributes are updated if the document ID exists.
        For more info, check https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html.
        """
        return requests.post(
            "{url}/{index}/_doc/{id}".format(url=self.url, index=self.index, id=data_point["id"]),
            json=data_point
        )

    def bulk_insert(self, data_points: typing.List[dict]) -> requests.Response:
        """Execute a bulk insert operation to process multiple events in a single request.
        Meta defines the type of bulk action to execute on each event.
        For more info, check https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html."""
        ndjson_data = (
            "\n".join(
                "{meta}\n{event}".format(
                    meta=json.dumps({"index": {"_id": data_point["id"]}}),
                    event=json.dumps(data_point),
                )
                for data_point in data_points
            )
            + "\n"
        )
        return requests.post(
            "{url}/{index}/_bulk".format(url=self.url, index=self.index),
            headers={"Content-Type": "application/x-ndjson"},
            data=ndjson_data
        )
