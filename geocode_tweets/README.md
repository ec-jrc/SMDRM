# Geocode Tweets

Search place candidates identified at [transform_tweets](../transform_tweets/README.md)
task against our Global Places datasets.

For more details on the Global Places dataset,
check [tools/locations/README.md](../tools/locations/README.md)

Execution
* create a subset of the Global Places dataset using the `region_id` argument
* create a `reference_keywords` key out of place names to search against
* geolocate Geo Political Entities (GPEs) place candidates only
* searches over multiple GPEs until it finds a match in the `reference_keywords`
* returns a (dict) serialized Place object with:
  * city coordinates when a single match exists
  * region bounding box centroid coordinates when multiple matches exist 

## Requirements

Docker Engine
Python 3.8
 - libdrm
 - pandas

> :bangbang: execute all bash commands from project root directory

## Build

```shell
./geocode_tweets/build.sh base
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -v $(pwd)/data:/data jrc/geocode_tweets_base
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project $SMDRM_HOME directory

```shell
docker container run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/geocode_tweets:/opt/smdrm/geocode_tweets \
  jrc/geocode_tweets_base \
  /bin/bash
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Tests

Build the Docker image for testing

```shell
./geocode_tweets/build.sh test
```

Run the unittests

```shell
docker container run -it --rm jrc/geocode_tweets_test tests/unit
```

## Releases

- **0.1.0**
  First Release

