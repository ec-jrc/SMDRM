# Extract Tweets

It minimizes the memory consumption footprint by removing unnecessary data.

Executes
* _not jsonl_: filter raw bytes that failed the JSON transformation
* _jsonl.get('tweet', jsonl)_: extract the raw Twitter datapoint if already processed
* _extend_text_field_: extract the most text from a given Twitter datapoint
* _DataPointModel.parse_obj_: parse specific fields from raw Twitter datapoint

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
