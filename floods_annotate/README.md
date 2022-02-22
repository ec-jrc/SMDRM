# Floods Annotate

Annotate `text` data with the Floods Named Entity Recognition annotator.

The annotator is trained to recognize floods related texts in a limited number
of languages.

It is accessible via HTTP REST API request. The expected input data is a batch
of texts of a single language.

Executes
* group batch by language
* HTTP call to Floods Annotator API

> :bangbang: execute all bash commands from project root directory

## Build

```shell
docker-compose build floods-annotate
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input zipfiles in the data/ directory
docker container run --rm -it --network host -v $(pwd)/data:/data floods-annotate
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
export ENV=dev
docker-compose run --rm -v $(pwd)/data:/data -v $(pwd)/floods_annotate:/opt/smdrm/floods_annotate floods-annotate bash 
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
docker-compose build floods-annotate
```

### Unittests

```shell
docker-compose run --rm floods-annotate tests/unit
```

## Releases

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release

