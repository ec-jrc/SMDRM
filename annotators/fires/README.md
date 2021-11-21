# Fires API

> :bangbang: **IMPORTANT NOTICE**
> 
> Currently, this annotator is under internal evaluation, and it has not had made available to the public yet.
> We will release it soon together with an official publication.
> 
> If you would like to use it before the official release,
> please contact [Valerio Lorini](mailto:valerio.lorini@ec.europa.eu?subject=[SMDRM]%20Fires%20Annotator%20Access).

Docker service based on [Python:3.8-slim-bullseye](https://github.com/docker-library/python/blob/9242c448c7e50d5671e53a393fc2c464683f35dd/3.8/bullseye/slim/Dockerfile) image.

It uses Machine Learning models trained on text related to fire disasters to annotate new incoming texts.
It requires `text` (the raw textual information to be annotated),
and `annotations` (the placeholder list to store annotation results) fields to be able to compute an annotation.

> :information_source: the `ANNOTATION_BATCH_SIZE` environment variable updates the annotation batch size

## Requisites

* Docker >= 19
* Python 3.8
  * [pip dependencies](requirements.txt)

The annotator model uses torch for preprocessing purposes.
We install the [CPU only wheel](https://download.pytorch.org/whl/torch/) to save resources.

## Download

You need to download the model, then run the Fires API.

Use this [download link](https://drive.google.com/drive/folders/1QBiJG73kwinsuE0Lr2pqN5WeMnegKhG9?usp=sharing) to
get the model binary files from the hosting cloud provider.

Ensure the following filesystem structure in the root level of the _models_ directory

```shell
# folder structure
fires/
  ...
  models/
    config.json
    optimizer.pt
    pytorch_model.bin
    scheduler.pt
    trainer_state.json
    trainer_args.bin
```

## Build & Run

Build and run the API

```shell
# executed from the project root directory
docker-compose up --build fires
```

## Usage

Test the API with the following synthetic data points

```shell
# note the `batch` and `annotations` fields in the payload
curl "http://localhost:5002" \
  -H "Content-Type: application/json" \
  -d '{"batch": {"texts": ["a string", "another string"]}}'
```

This should return the batch, enriched with the annotations

```shell
{
  "batch": {
    "texts": [
      "a string",
      "another string",
    ],
    "annotation_probs": [
      "float",
      "float",
    ],
    "annotation_type": "fires",
}
```

Clean Up

```shell
docker container rm -f fires
```

## Tests

Build the [test](Dockerfile) Docker image

```shell
cd annotators/fires && docker build --target test -t firesapi:test . && cd -
```

### Unit

Run the unit tests

> :warning: This task is slow due to the time to load the annotation model

```shell
cd annotators/fires && docker container run --rm -v $(pwd)/models:/app/models firesapi:test tests/unit && cd -
```

### Integration

Initialize the test instance of the API

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build fires
```

Run the integration tests

```shell
# note the network flag (see docker-compose.tests.yml)
docker container run --rm --network smdrm_tests firesapi:test tests/integration
```

Clean up

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml down
```

