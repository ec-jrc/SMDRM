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
docker-compose build transform-tweets
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input zipfiles in the data/ directory
docker container run --rm -it --network host -v $(pwd)/data:/data transform-tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
export ENV=dev
docker-compose run --rm -v $(pwd)/data:/data -v $(pwd)/transform_tweets:/opt/smdrm/transform_tweets transform-tweets bash
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
docker-compose build transform-tweets
```

### Unittests

```shell
docker-compose run --rm transform-tweets tests/unit
```

## Releases

- **0.1.5**
  Place candidate extraction discards non-alphanumeric characters.
  Transformations include Twitter Retweeted `RT` flag removal.

- **0.1.4**
  Code refactoring that leverages the Pipe and Filter design pattern.
  Transformation steps are now organized into an ad hoc pipeline.

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

