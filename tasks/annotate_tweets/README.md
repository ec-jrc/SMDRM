# Annotate Tweets

Annotate `text` data with a chosen Named Entity Recognition annotator.

Execution
* Batch datapoints
* HTTP POST call to Annotator API

## Annotator

The annotator is trained to recognize natural disaster related texts.
It is accessible via HTTP REST API request to the dedicated Docker container.

The expected input data is a batch of texts in any language.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)&nbsp;&nbsp;![Requests](https://img.shields.io/badge/Requests-~=2.27-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build annotate-tweets
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

```shell
# add your input zipfiles in the data/ directory
docker-compose run --rm -v $(pwd)/data:/data annotate-tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /home/smdrm inside the container.

```shell
docker-compose run --rm \
    -v $(pwd)/data:/data \
    -v $(pwd)/annotate_tweets:/home/smdrm/annotate_tweets \
    annotate-tweets \
    /bin/bash
```

Or, you can start a [Jupyter Notebook session](../libdrm/README.md#development).

## Test

Run the unittests

```shell
docker-compose run --rm annotate-tweets pytest
```

## Releases

- **0.1.2**
  Annotator independent task. Annotator is now passed as ANNOTATOR_ID env variable.
  This is the hostname used to build the base URL to send the HTTP POST request to.

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release

