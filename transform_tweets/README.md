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

```shell
./transform_tweets/build.sh
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -v $(pwd)/data:/data jrc/transform_tweets_base
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project $SMDRM_HOME directory

```shell
docker container run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/transform_tweets:/opt/smdrm \
  jrc/transform_tweets_base \
  /bin/bash
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Test

Build the Docker image for testing

```shell
./transform_tweets/build.sh test
```

Run the unittests

```shell
docker container run -it --rm jrc/transform_tweets_test tests/unit
```

## Releases

- **0.1.2**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.1**
  Transformation does not takes into account batch duplicates when sending texts
  to DeepPavlov REST API. This is intended to improve task performance.

- **0.1.0**
  First Release
