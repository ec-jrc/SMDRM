# Floods Annotate

Annotate `text` data with the Floods Named Entity Recognition annotator.

The annotator is trained to recognize floods related texts in a limited number
of languages.

It is accessible via HTTP REST API request. The expected input data is a batch
of texts of a single language.

Execution
* group batch by language
* HTTP call to Floods Annotator API

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)&nbsp;&nbsp;![Pandas](https://img.shields.io/badge/Pandas-1.3.5-information)&nbsp;&nbsp;![Requests](https://img.shields.io/badge/requests-2.27.0-information)

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
to the project directory /opt/smdrm inside the container.

```shell
export ENV=dev
docker-compose run --rm -v $(pwd)/data:/data -v $(pwd)/floods_annotate:/opt/smdrm/floods_annotate floods-annotate bash 
```

Or, starting a Jupyter Notebook session

```shell
export ENV=dev
docker-compose run --rm -v $(pwd):/opt/smdrm/ws -w /opt/smdrm/ws libdrm bash tools/dev.sh
```

## Test

Build the Docker image for testing

```shell
export ENV=test
docker-compose build floods-annotate
```

### Unittests

```shell
docker-compose run --rm floods-annotate tests/unit
```

## Releases

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release

