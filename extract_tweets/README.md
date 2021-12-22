# Extract Tweets

It minimizes the memory consumption footprint by removing unnecessary data.

Executes
* ...
* ...

> :bangbang: execute all bash commands from project root directory

## Build

```shell
./extract_tweets/build.sh
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -v $(pwd)/data:/data jrc/extract_tweets_base
```

## Develop

You can develop in a standardized environment using Jupyter Notebook.

```shell
./start_dev.sh
```

## Tests

```shell
./extract_tweets/build.sh test && ./extract_tweets/test.sh
```
