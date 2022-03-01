# Cache Tweets

Caches the content of a zipfile of enriched datapoints
that passed through the tasks of a pipeline (DAG) to ElasticSearch.

You can use the Kibana UI to manage the cached datapoints.

Execution
* initializes an instance of the Elasticsearch Python package
* creates an index with _smdrm\__ prefix using index and component templates
* triggers a bulk insert API call to cache the enriched Twitter based datapoints

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)&nbsp;&nbsp;![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.0.0-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build cache-tweets
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

```shell
# add your input zipfiles in the data/ directory
docker-compose run --rm -v $(pwd)/data:/data cache-tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /home/smdrm inside the container.

```shell
docker-compose run --rm \
    -v $(pwd)/data:/data \
    -v $(pwd)/cache_tweets:/home/smdrm/cache_tweets \
    cache-tweets \
    bash
```

Or, you can start a [Jupyter Notebook session](../libdrm/README.md#development).

## Tests

Run the unittests

```shell
docker-compose run --rm cache-tweets pytest
```

## Releases

- **0.1.0**
  First Release

