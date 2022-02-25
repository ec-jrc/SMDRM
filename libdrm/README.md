# LibDRM

LibDRM holds the core functionality required by the tasks of the SMDRM Pipeline.
For additional details on the tasks, check the [airflow/README.md](https://github.com/ec-jrc/SMDRM/blob/main/airflow/README.md) section.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![Pydantic](https://img.shields.io/badge/Pydantic-~=1.8-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build libdrm
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

This Docker image is used as base image to build, and develop the SMDRM Pipeline tasks.
It is not supposed to be run directly, unless for development purposes.

## Development

Enter the SMDRM Python interpreter

```shell
export ENV=dev
docker-compose run --rm libdrm
```

Start a Jupyter Notebook and mount the project folder for dynamic modifications
without the need to rebuild the image every time.

```shell
export ENV=dev
docker-compose run --rm -v $(pwd):/opt/smdrm/ws -w /opt/smdrm/ws libdrm bash tools/dev.sh
```

## Tests

```shell
export ENV=test
docker-compose build libdrm
```

Run the unittests

```shell
docker-compose run --rm libdrm tests/unit
```

## Modules

### Common

Usable by all tasks

### Datamodels

Consistent structure of input/output data

* `DataPointModel`
* `ZipFileModel`

### Elastic

This module contains a custom ElasticSearch Client that performs the following API operations:
* create index template
* create/delete index
* add document
* add document batch

It also contains the ElasticSearch Template Mappings definition to set the data structure of indexed data points.

### Pipelines

Pipeline Class creates ad hoc data processing pipeline using generators and OOP.

It also defines the required fields of the Disaster (data point) Model via
the `DisasterModel` Class using [Pydantinc](https://pydantic-docs.helpmanual.io/).

## Publish

GitHub Action.

## Releases

- **0.1.10**
  New DataPointModel data structure:
   * include legacy fields
   * better field naming

- **0.1.9**
  Remove hardcoded metrics generation from `ZipFileModel.cache()` method.
  It is now task responsibility to include them in the pipeline steps.  

- **0.1.8**
  `ZipFileModel.cache()` method now expects a generator of NDJSON batches.

- **0.1.7**
  Optional fields `text_clean`, and `places` in `DataPointModel` class set to `None`.
  This allows failure when those fields are screened under certain conditions.
  For instance, `cnn_texts = g.text_clean.values.tolist()` in
  _floods_annotate/src/floods_annotate.py_

