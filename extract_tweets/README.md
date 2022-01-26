# Extract Tweets

It minimizes the memory consumption footprint by removing unnecessary data.

Executes
* _not jsonl_: filter raw bytes that failed the JSON transformation
* _jsonl.get('tweet', jsonl)_: extract the raw Twitter datapoint if already processed
* _extend_text_field_: extract the most text from a given Twitter datapoint
* _DataPointModel.parse_obj_: parse specific fields from raw Twitter datapoint

> :bangbang: execute all bash commands from project root directory

## Build

Make sure to select the intended environment with ENV variable in [.env](../.env).

```shell
./build_task.sh extract_tweets
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -it -v $(pwd)/data:/data smdrm/extract_tweets
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
docker container run --rm -it \
  -v $(pwd)/data:/data \
  -v $(pwd)/extract_tweets:/opt/smdrm/extract_tweets \
  smdrm/extract_tweets
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Tests

Build the Docker image for testing

```shell
# ENV=test in .env
./build_task.sh extract_tweets
```

Run the unittests

```shell
docker container run --rm -it smdrm/extract_tweets tests/unit
```

## Releases

- **0.1.1**
  Code refactory to use clearer pipeline step approach.

- **0.1.0**
  First Release

