# Annotate Tweets

Annotate `text` data with Named Entity Recognition algorithms.

Executes
* ...
* ...

> :bangbang: execute all bash commands from project root directory

## Build

```shell
./annotate_tweets/build.sh
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -v $(pwd)/data:/data jrc/floods_annotate_base
```

## Develop

You can develop in a standardized environment using Jupyter Notebook.

```shell
./start_dev.sh
```

## Test

Run the unittests

```shell
./floods_annotate/build.sh test && ./floods_annotate/test.sh
```
