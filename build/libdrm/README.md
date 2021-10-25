# LIBDRM

Python based modules representing the core functionality of the SMDRM application.

Currently, there are four core modules:
* [apis.py](src/libdrm/apis.py)
* [elastic.py](src/libdrm/elastic.py)
* [pipeline.py](src/libdrm/pipeline.py)
* [schemas.py](src/libdrm/schemas.py)

## [Apis](src/libdrm/apis.py)

This module holds information on available APIs to execute operations such as annotation and caching of data points.

It contains a lookup table with url instructions to contact them. Finally, it implements functions to check/wait on
their current statuses. The latter is particularly useful during SMDRM application microservice start up.

## [Elastic](src/libdrm/elastic.py)

This module contains a custom ElasticSearch Client that performs the following API operations:
* create index template
* create/delete index
* add document
* add document batch

It also contains the ElasticSearch Template Mappings definition to set the data structure of indexed data points.

## [Pipeline](src/libdrm/pipeline.py)

SMDRM Data Processing Pipeline enables the creation of ad hoc data processing pipeline 
with regard to the task at hand using a combination of Template and Bridge Design Patterns.

It also defines the required fields of the Disaster (data point) Model via
the DisasterModel Class using [Pydantinc](https://pydantic-docs.helpmanual.io/).

A custom sequence of pipeline Steps can be used to make a pipeline to process input data.

The most important steps include:
* read zip files
* read JSON files (inside the zip file)
* validate/parse JSON file content
* read JSON file content in batches (useful for annotation)

## [Schemas](src/libdrm/schemas.py)

This module uses [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) data model schemas to validate
the uploaded zip file and metadata.
It ensures the validity of the user input data, preventing any invalid data to enter the data processing pipeline.
