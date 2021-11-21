# Floods API

Docker service based on [Python:3.8-slim-bullseye](https://github.com/docker-library/python/blob/9242c448c7e50d5671e53a393fc2c464683f35dd/3.8/bullseye/slim/Dockerfile) image.

It uses Machine Learning models trained on text related to flood disasters to annotate new incoming texts.
It requires `lang` and `text` fields to be able to compute an annotation.

> :information_source: the `ANNOTATION_BATCH_SIZE` environment variable updates the annotation batch size.

## Requirements

* Python 3.8
  * [pip dependencies](requirements.txt)

The annotator model uses torch for preprocessing purposes.
We install the [CPU only wheel](https://download.pytorch.org/whl/torch/) to save resources.

## Download

Enable the [Development Environment](https://github.com/panc86/smdrm/blob/master/dev/README.md)
```shell
bash dev/run.sh
```

Then execute the following command in the shell
```shell
bash annotators/floods/downloads.sh
```

The flag `--clear` deletes any models previously downloaded

## Build & Run

Build and run the FloodsAPI
```shell
docker-compose up --build floods
```

## Usage

Test the API with the following synthetic data points

> :information_source: Note the "batch" key in the payload.

```shell
curl "http://localhost:5001" \
  -H "Content-Type: application/json" \
  -d '{"batch": {"lang": "en", "texts": ["a flood disaster text url","another flood disaster text url"]}}'
```

This should return the same data points being sent, enriched with `text_sanitized` and `annotation` fields

```shell
{
  "batch": {
    "lang": "en",
    "texts": [
      "a flood disaster text url",
      "another flood disaster text url",
    ],
    "annotation_probs": [
      "0.022930",
      "0.006453",
    ],
    "annotation_type": "fires",
}
```

Clean Up

```shell
# stop with `CTRL+C`.
docker container rm -f floods
```

## Tests

Build the [test](Dockerfile) Docker image

```shell
cd annotators/floods && docker build --target test -t floodsapi:test . && cd -
```

### Unit

Run the unit tests

```shell
cd annotators/floods && docker container run --rm -v $(pwd)/models:/app/models floodsapi:test tests/unit && cd -
```

### Integration

Initialize the test instance of the API

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build floods
```

Run the integration tests

```shell
# note the network flag (see docker-compose.tests.yml)
docker container run --rm --network smdrm_tests floodsapi:test tests/integration
```

Clean up

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml down
```
