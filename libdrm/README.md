# LibDRM

It holds the core functionality required by SMDRM Pipeline tasks.

For more details, go to the [source code](https://github.com/panc86/smdrm/tree/master/libdrm) on GitHub.

> :bangbang: execute all bash commands from project root directory

## Build

Make sure to select the intended environment with ENV variable in [.env](../.env).

```shell
./build_task.sh libdrm
```

For more details, check the [Dockerfile](Dockerfile).

## Development

Build a Jupyter Notebook development environment using the `ENV=dev`
environment variable in .env.

```shell
# ENV=dev in .env
./build_task.sh libdrm
```

Mount your data, and the directory with the source code under development.
Changes to the source code will be applied to the source code in the container
without need to restart.

```shell
./start_dev.sh
```

## Tests

Run the unittests

```shell
docker container run -it --rm smdrm/libdrm tests/unit
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
