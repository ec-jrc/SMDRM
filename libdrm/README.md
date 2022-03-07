# LibDRM

LibDRM Python package holds the core functionality required by the tasks of the SMDRM Pipeline.
For additional details on the tasks, check the [airflow/README.md](https://github.com/ec-jrc/SMDRM/blob/main/airflow/README.md) section.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![Pydantic](https://img.shields.io/badge/Pydantic-~=1.8-information)&nbsp;&nbsp;![Pytest](https://img.shields.io/badge/Pytest-~=7.0-information)

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

Start a Jupyter Notebook and mount the project folder for dynamic modifications
without the need to rebuild the image every time.

```shell
docker-compose run --rm -v $(pwd):/home/smdrm/ws libdrm bash ws/tools/dev.sh
```

## Tests

Run the unittests

```shell
docker-compose run --rm libdrm pytest libdrm/tests
```

## Modules

### Common

Usable by all tasks

### Datamodels

* `DataPointModel`
* `ZipFileModel`

`DataPointModel` [Pydantic](https://pydantic-docs.helpmanual.io/) Class object is
a representation of a natural disaster datapoint. It defines required fields, and
inherits validation as well as raw data parsing capabilities.

`ZipFileModel` Class object is a representation of a zipfile parser. It enables
reading, writing, and validation capabilities for zipfiles of any size.

### Pipelines

Provides a OOP data processing pipeline.

## Releases

- **0.1.10**
  New DataPointModel fields:
   * include legacy fields
   * clearer field naming

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
