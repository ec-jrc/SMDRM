# Transform Tweets

Transform data point `text` field.

## Transformations

* mentions
* URLs
* hashtags
* punctuation
* white spaces
* new lines
* dates

> :bangbang: execute all bash commands from project root directory

## Build

Make sure to select the intended environment with ENV variable in [.env](../.env).

```shell
./build_task.sh transform_tweets
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -it -v $(pwd)/data:/data smdrm/transform_tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
docker container run --rm -it \
  -v $(pwd)/data:/data \
  -v $(pwd)/transform_tweets:/opt/smdrm/transform_tweets \
  smdrm/transform_tweets
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Test

Build the Docker image for testing

```shell
# ENV=test in .env
./build_task.sh transform_tweets
```

Run the unittests

```shell
docker container run --rm -it smdrm/transform_tweets tests/unit
```

## Releases

- **0.1.3**
  Place candidate extraction and output datamodel refactoring.

- **0.1.2**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.1**
  Transformation does not takes into account batch duplicates when sending texts
  to DeepPavlov REST API. This is intended to improve task performance.

- **0.1.0**
  First Release

