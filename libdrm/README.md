# LibDRM

It holds the core functionality required by SMDRM Pipeline tasks.

For more details, go to the [source code](https://github.com/panc86/smdrm/tree/master/libdrm) on GitHub.

> :bangbang: execute all bash commands from project root directory

## Build

```shell
# By default, build the base image
./libdrm/build.sh
```

For more details, check the [Dockerfile](Dockerfile).

## Development

Build a Jupyter Notebook development environment using the `dev` stage.

```shell
./libdrm/build.sh dev
```

Mount your data, and the directory with the source code under development.
Changes to the source code will be applied to the source code in the container
without need to restart.

```shell
docker run -it --rm \
  -e JUPYTER_TOKEN=docker \
  --network host \
  # add data
  --volume $(pwd)/data:/opt/smdrm/data \
  # code changes without container restart
  --volume $(pwd)/libdrm:/opt/smdrm/libdrm \
  # keep track of development history
  --volume $(pwd)/nbs:/opt/smdrm/nbs \
  jrc/smdrm_dev
```

> :bangbang: DO NOT forget to rebuild the `jrc/smdrm_dev`

## Tests

Run the unittests

```shell
./libdrm/build.sh test && ./libdrm/test.sh
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

- **0.1.8**
  `ZipFileModel.cache()` method now expects a generator of NDJSON batches.

- **0.1.7**
  Optional fields `text_clean`, and `places` in `DataPointModel` class set to `None`.
  This allows failure when those fields are screened under certain conditions.
  For instance, `cnn_texts = g.text_clean.values.tolist()` in
  _floods_annotate/src/floods_annotate.py_
