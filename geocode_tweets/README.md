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

Make sure to select the intended environment with ENV variable in [.env](../.env).

```shell
./build_task.sh geocode_tweets
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
# add --network host if ENV=dev
docker container run --rm -it -v $(pwd)/data:/data smdrm/geocode_tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
docker container run --rm -it \
  --network host \
  -v $(pwd)/data:/data \
  -v $(pwd)/geocode_tweets:/opt/smdrm/geocode_tweets \
  smdrm/geocode_tweets
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Tests

Build the Docker image for testing

```shell
# ENV=test in .env
./build_task.sh geocode_tweets
```

Run the unittests

```shell
docker container run --rm -it smdrm/geocode_tweets tests/unit
```

## Releases

- **0.1.0**
  First Release

