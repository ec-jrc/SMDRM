# LIBDRM Package

Python based modules representing the core functionality of the SMDRM application.

Currently, there are four core modules:
* [apis.py](#APIs)
* [elastic.py](#elastic)
* [pipeline.py](#pipeline)
* [schemas.py](#schemas)

For more info, go to the [source code](https://github.com/panc86/smdrm/tree/master/libdrm) on GitHub.

## Modules

### APIs

This module holds information on available APIs to execute operations such as annotation and caching of data points.

It contains a lookup table with url instructions to contact them. Finally, it implements functions to check/wait on
their current statuses. The latter is particularly useful during SMDRM application microservice start up.

### Elastic

This module contains a custom ElasticSearch Client that performs the following API operations:
* create index template
* create/delete index
* add document
* add document batch

It also contains the ElasticSearch Template Mappings definition to set the data structure of indexed data points.

### Pipeline

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

### Schemas

This module uses [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) data model schemas to validate
the uploaded zip file and metadata.
It ensures the validity of the user input data, preventing any invalid data to enter the data processing pipeline.


## Publish

For more info, check the [publish.yml](https://github.com/panc86/smdrm/blob/master/.github/workflows/publish.yml) GitHub Action.


## Releases

- 0.1.3: added pipeline step to parse legacy data points wrapped in a `tweet` field.
