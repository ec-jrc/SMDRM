# Text Normalize API

Docker service based on [Python:3.8-slim-bullseye](https://github.com/docker-library/python/blob/9242c448c7e50d5671e53a393fc2c464683f35dd/3.8/bullseye/slim/Dockerfile) image.
It normalizes the annotation input data, i.e. data point `text` attribute.

## Normalizations

Normalization tasks covers:

* user mention (anonymize)
* URLs
* hashtags
* punctuation
* white spaces
* new lines
* dates


## Build & Run

```shell
# executed from the project root directory
docker-compose up --build text-normalize
```

Now the API should be up and running.

## Usage

Test the API with the following synthetic data points

```shell
# note the "batch" key in the payload
curl -v -X POST http://localhost:5050 \
    -H "Content-Type: application/json" \
    -d '{"batch": ["RT \na text string,   &amp; to be normalized @API #NothingSpecial https://example.com http"]}'
```

This should return the batch of normalized texts

```shell
{
    "text_normalized": [
        "a text string and to be normalized nothingspecial url"
    ]
}
```

## Clean Up

You can stop a running instance of the API simply with `CTRL+C`.

Execute the following command to remove the service

```shell
docker container rm -f text-normalize
```

## Tests

Build the [test Docker image](Dockerfile.tests)

```shell
cd transformers/text_normalize
docker build -f Dockerfile.tests -t textnormalizeapi:test .
cd -
```

### Unit

Run the unit tests

```shell
docker container run --rm textnormalizeapi:test tests/unit
```

### Integration

Initialize the test instance of the API

```shell
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build text-normalize
```

Run the integration tests

```shell
# note the network flag (see docker-compose.tests.yml)
docker container run --rm --network smdrm_tests textnormalizeapi:test tests/integration
```

Clean up

```shell
docker-compose -f docker-compose.yml -f docker-compose.tests.yml down
```
