# Transform Tweets

Appy normalization transformations on the datapoint `text` field,
and extracts place candidates for geocoding purposes with [DeepPavlov](https://deeppavlov.ai/).

Execution
* remove user mentions
* normalize URLs
* normalize hashtags
* remove punctuation
* remove retweets
* normalize white spaces
* remove new lines
* remove dates
* tag place candidates

## Annotator

DeepPavlov annotator uses a pre-trained model for multilingual geolocation tagging.
It is accessible via HTTP REST API request to the dedicated Docker container.

The expected input data is a batch of texts.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![LibDRM](https://img.shields.io/badge/libdrm-latest-information)&nbsp;&nbsp;![Requests](https://img.shields.io/badge/Requests-~=2.27-information)&nbsp;&nbsp;![Pandas](https://img.shields.io/badge/Pandas-~=1.4-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build transform-tweets
```

For additional details, check the [Dockerfile](Dockerfile).

### Run

```shell
# add your input zipfiles in the data/ directory
docker-compose run --rm -v $(pwd)/data:/data transform-tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /home/smdrm inside the container.

```shell
docker-compose run --rm \
    -v $(pwd)/data:/data \
    -v $(pwd)/transform_tweets:/home/smdrm/transform_tweets \
    transform-tweets \
    /bin/bash
```

Or, you can start a [Jupyter Notebook session](../libdrm/README.md#development).

## Test

Run the unittests

```shell
docker-compose run --rm transform-tweets pytest
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

