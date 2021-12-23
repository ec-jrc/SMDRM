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

You can develop in a standardized environment using Jupyter Notebook.

```shell
./start_dev.sh
```

## Test

Run the unittests

```shell
./transform_tweets/build.sh test && ./transform_tweets/test.sh
```
