# Airflow

> Airflow is a platform to programmatically author, schedule and monitor workflows.
> Use Airflow to author workflows as Directed Acyclic Graphs (DAGs) of tasks.
> Source [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/2.2.3/index.html#apache-airflow-documentation).

For additional info of DAGs, workflows, and tasks, check the relative sections in the [glossary](../docs/glossary.md). 

## Twitter DAG

The `twitter` DAG is a workflow of tasks tailored to extract, transform,
[annotate](../docs/glossary.md#annotate), and geocode Twitter [datapoints](../docs/glossary.md#datapoint).

Each task in this DAG takes an input zipfile, executes a data processing logic,
and returns an enriched output.

> :information_source: Currently, only the `twitter` DAG is operational.

### Tasks

Table 1 shows the `twitter` DAG _tasks_

|Name|Description|
|----|-----------|
|`extract-tweets`|Extracts required fields from raw data, and generates new fields to create the Datapoint model.|
|`transform-tweets`|Apply place and grammar normalization transformations to clean the `text` field and identify place candidates.|
|`annotate-tweets`|Assign a (natural) disaster related probability score to the datapoint given its (cleaned) `text`, and the chosen ANNOTATOR_ID env.|
|`geocode-tweets`|Assign latitude and longitude coordinates to the datapoint whose place candidates matches against a [GADM](https://gadm.org) based [Global Places gazettier](geocode_tweets/config/global_places_v1.tsv).|
|`cache-tweets`|Cache geocoded datapoints to Elasticsearch database.|

_Table 1. Twitter DAG Tasks_

### External Plugins

Table 2 shows the external plugins the Twitter DAG uses to enrich the input datapoints

|Name|Image|URL|Responsibilities|
|----|-----|---|----------------|
|[DeepPavlov API](annotators/deeppavlov/README.md)|[_deeppavlov_](annotators/deeppavlov/Dockerfile)|`http:/deeppavlov:5000`|DeepPavlov NER REST API for geo political, location, and facility entity tagging.|
|[Floods API](annotators/floods/README.md)|[_floods_](annotators/floods/Dockerfile)|`http://floods:5000`|Floods NER REST API to annotate floods disaster type related datapoints.|

_Table 2. External Plugins_

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![Airflow](https://img.shields.io/badge/Airflow-2.2.3-information)

> :bangbang: Execute all bash commands from project root directory

### Build

Build the Docker image

```shell
docker-compose --profile pipelines build
```

### Run

Initialize the Airflow DB and run the Airflow components

```shell
docker-compose up airflow-init && docker-compose up
```

You should see the following entries in the list of running containers (`docker-compose ps`)

e airflow-scheduler
- airflow-triggerer
- airflow-worker
- airflow-webserver
- docker-proxy
- flower
- postgres
- redis

### Run a DAG

1. put your zipfile in ./data/youfile.zip
2. copy your zipfile in the Docker Volume smdrm_uploads-volume i.e. created with docker-compose up

```shell
docker-compose run --rm -v smdrm_uploads-volume:/output -v $(pwd)/data:/input libdrm cp /input/youfile.zip /output
```

3. trigger a DAG run with Config via the CLI

```shell
# Twitter DAG --conf '{"COLLECTION_ID": "smdrm_uploads-volume", "INPUT_PATH": "/data/youfile.zip"}'
docker-compose run --rm airflow-cli airflow dags trigger <dag_ID> --conf '{"key": "value"}' --run-id <helps-you-identify-this run>
```

Alternatively, you can trigger a DAG run from the UI.

## UI

Go to the [Airflow UI](http://localhost:8080)

Default credentials are:
* USERNAME=airflow
* PASSWORD=airflow

You can monitor DAGs execution, and investigate failures for each task.

## Tests

Airflow tests are divided as follows:

* Validation
* Unit
* Integration
* Acceptance (E2E)

### Validation

```shell
docker-compose run --rm airflow-cli bash -c pytest
```

## Develop

Run the airflow-cli to spin an airflow CLI ready shell

You can use the CLI to trigger DAGs and individual tasks for testing purposes. 
For instance, we test the Elasticsearch API sensor task as follows:

```shell
docker-compose run --rm airflow-cli airflow tasks test twitter is_elasticsearch_api_ready 2022-01-01
```

## Enable Emails Notification

Add the following environment variables in an .env file and save it into the project root directory.

Say, you have a Google Mail account and you want to use that to send notifications out.

```shell
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=youremail@gmail.com
SMTP_PASSWORD=smtp-provider-auth-token*
CSV_EMAILS_TO_NOTIFY_FAILURES=emails to send notifications to
```

\*search for 'google app password'
