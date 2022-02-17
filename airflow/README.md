# Airflow

Orchestrates the tasks of the SMDRM data processing pipeline.
A new instance is created for each dataset (collection) to be processed.

> :bangbang:
> * execute all bash commands from project root directory
> * replace <variables> with your values

## Requisites

Docker
Python

The input of a DAG is the output of a collection. Each collection in the Collections UI
creates, and caches an output zipfile into a Docker Volume every 15 minutes.
The collection ID is the name of the Docker Volume.

The Docker Volume filesystem is structured as follows:

```text
-date
 |
 -time
  |
  -file.zip
```

Where,
* `date`=`YYYYMMDD`
* `time`=`HHMM` (UTC)


## Build

Build the Docker image

```shell
docker-compose build
```

## Run

First initialize the DB

```shell
docker-compose up airflow-init
```

Then, run the service

```shell
docker-compose up
```

Finally, you should see the following containers by running `docker-compose ps`

- airflow-scheduler
- airflow-triggerer
- flower
- airflow-worker
- airflow-webserver
- docker-proxy 
- postgres      
- redis          

## UI

Airflow UI is now available at http://localhost:8080 

## Develop

Execute the airflow running container to spin the shell,
and be able to run airflow CLI locally

```shell
docker-compose run --rm airflow-cli bash
```

## Run a DAG

Trigger a manual DAG run

Steps
1. copy your zipfile in ./data/imports/
2. execute `trigger-dag-run` docker container as follows

```shell
docker-compose build trigger-dag-run && docker-compose run --rm trigger-dag-run
```
3. wait for the process execution
4. collect your artifact data at ./data/exports/

