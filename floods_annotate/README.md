# Floods Annotate

Annotate `text` data with the Floods Named Entity Recognition annotator.

Execution
* group batch by language
* HTTP call to Floods Annotator API

## Annotator

The annotator is trained to recognize floods related texts in a limited number
of languages. It is accessible via HTTP REST API request to the dedicated Docker container.

The expected input data is a batch of texts of a single language.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)&nbsp;&nbsp;![Requests](https://img.shields.io/badge/Requests-~=2.27-information)&nbsp;&nbsp;![Pandas](https://img.shields.io/badge/Pandas-~=1.4-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build floods-annotate
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

```shell
# add your input zipfiles in the data/ directory
docker-compose run --rm -v $(pwd)/data:/data floods-annotate
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /home/smdrm inside the container.

```shell
docker-compose run --rm \
    -v $(pwd)/data:/data \
    -v $(pwd)/floods_annotate:/home/smdrm/floods_annotate \
    floods-annotate \
    /bin/bash
```

Or, you can start a [Jupyter Notebook session](../libdrm/README.md#development).

## Test

Run the unittests

```shell
docker-compose run --rm floods-annotate pytest
```

## Releases

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release

