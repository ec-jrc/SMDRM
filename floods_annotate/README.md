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

Make sure to select the intended environment with ENV variable in [.env](../.env).


```shell
./build_task.sh floods_annotate
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
# add --network host if ENV=dev
docker container run --rm -it -v $(pwd)/data:/data smdrm/floods_annotate
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project directory /opt/smdrm inside the container.

```shell
docker container run --rm -it \
  --network host \
  -v $(pwd)/data:/data \
  -v $(pwd)/floods_annotate:/opt/smdrm/floods_annotate \
  smdrm/floods_annotate
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Test

Build the Docker image for testing

```shell
# ENV=test in .env
./build_task.sh floods_annotate
```

Run the unittests

```shell
docker container run --rm -it smdrm/floods_annotate tests/unit
```

## Releases

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release

