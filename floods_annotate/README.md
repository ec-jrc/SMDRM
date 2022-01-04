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
./annotate_tweets/build.sh
```

For more details, check the [Dockerfile](Dockerfile).

## Run

```shell
# add your input data in the data/ directory
docker container run --rm -v $(pwd)/data:/data jrc/floods_annotate_base
```

## Develop

You can develop in a standardized environment by mounting this directory
to the project $SMDRM_HOME directory

```shell
docker container run -it --rm \
  -v $(pwd)/data:/data \
  -v $(pwd)/floods_annotate:/opt/smdrm \
  jrc/floods_annotate_base \
  /bin/bash
```

Or, project wide using Jupyter Notebook

```shell
./start_dev.sh
```

## Test

Build the Docker image for testing

```shell
./floods_annotate/build.sh test
```

Run the unittests

```shell
docker container run -it --rm jrc/floods_annotate_test tests/unit
```

## Releases

- **0.1.1**
  Removed Click Python package dependency. This makes Docker image creation
  faster and easier for any stage as it is no longer needed to build it as package.
  Introduced unit/integration tests separation logic.

- **0.1.0**
  First Release
