# Extract Tweets

Extracts/creates specific [fields](../docs/architecture.md#fields) to create a SMDRM [datapoint](../docs/glossary.md#datapoint).
It minimizes the memory consumption footprint by removing unnecessary data.

Execution
* filter raw bytes that failed the JSON transformation
* extract raw Twitter datapoint if already processed
* extract the most text from a given Twitter datapoint
* parse specific fields from raw Twitter datapoint

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build extract-tweets
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

```shell
# add your input zipfiles in the data/ directory
docker-compose run --rm -v $(pwd)/data:/data extract-tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
export ENV=dev
docker-compose run --rm -v $(pwd)/data:/data -v $(pwd)/extract_tweets:/opt/smdrm/extract_tweets extract-tweets bash
```

Or, starting a Jupyter Notebook session

```shell
export ENV=dev
docker-compose run --rm -v $(pwd):/opt/smdrm/ws -w /opt/smdrm/ws libdrm bash tools/dev.sh
```

## Tests

Build the Docker image for testing

```shell
export ENV=test
docker-compose build extract-tweets
```

### Unittests

```shell
docker-compose run --rm extract-tweets tests/unit
```

## Releases

- **0.1.1**
  Code refactory to use clearer pipeline step approach.

- **0.1.0**
  First Release

