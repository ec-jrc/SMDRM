"""
ElasticSearch Index Templates for SMDRM

There are two types of templates: index templates and component templates
* Index templates are a way to tell Elasticsearch how to configure an index when it is created.
* Component templates are reusable building blocks that configure indexes mappings, settings, and aliases.

Notes
    When you set "dynamic":"true", Elasticsearch will map string fields as a text field with a keyword subfield.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html#_structured_search
"""

# component templates
smdrm_component_template_config = {
    "name": "smdrm_component_template_base",
    "meta": {"description": "SMDRM component template"},
    "version": "1",
    "master_timeout": "10s",
    "template": {
        "mappings": {
            "_source": {"enabled": "true"},
            # new fields are not added automatically at root level
            # unless they are manually included in properties
            "dynamic": "strict",
            # annotations
            "dynamic_templates": [
                {
                    "annotations_as_float": {
                        "match_mapping_type": "string",
                        "path_match": "annotation.*",
                        "mapping": {"type": "float"},
                    }
                }
            ],
            "properties": {
                # required fields
                "created_at": {
                    "type": "date",
                    # Twitter date format
                    "format": "EEE LLL dd HH:mm:ss Z yyyy",
                },
                "id": {
                    "type": "text",
                },
                "lang": {"type": "keyword"},
                "text": {"type": "text"},
                "tags": {"type": "keyword"},
                # annotation field is dynamic wrt the annotation model
                "annotation": {"dynamic": "true", "type": "object"},
                # transformation fields
                "text_clean": {
                    # non-searchable
                    "index": "false",
                    "type": "text",
                },
                "place": {
                    # keep relationships among values of nested subfields
                    "type": "nested",
                    "properties": {
                        # candidates is dynamic wrt the place candidates matching
                        "candidates": {"dynamic": "true", "type": "object"},
                        # meta is dynamic wrt the place candidate type matched (city or region)
                        "meta": {"dynamic": "true", "type": "object"},
                    },
                },
            },
        }
    },
}

# index template
smdrm_index_template_config = {
    "name": "smdrm_index_template",
    "index_patterns": [
        "smdrm*",
    ],
    "template": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
    },
    "version": "1",
    "priority": 500,
    "composed_of": [
        "smdrm_component_template_base",
    ],
    "meta": {"description": "SMDRM index template"},
}
