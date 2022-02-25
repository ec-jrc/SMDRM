# Developer's Note

Notes on current and future development.

## Collections UI

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

## Annotator Endpoint Format

The API endpoint format is `http://<host>:<port>/<resource>`
The `host` variable depends on the location where an HTTP call is executed.
The `port` ranges for annotators is `5010-5050`.

## Add a new Annotator API

Table 1 lists the sequence of steps to implement a new annotator API.

> :information_source: The following steps are executed inside the annotators/ directory.
> Use other annotators as template to build your own annotator.

|Step|Action|Notes|
|---:|------|-----|
|1|Create a new directory `annotators/<new-annotator>/`| |
|2|Download/Create the trained Machine Learning prediction model into `annotators/<newapi>/models/`| |
|3|Create new api.py file with Flask| |
|4|Set the instructions to build a new Docker image in a new Dockerfile|Ensure to create a mountable volume to allow the user to caache heavy model downloads.|
|5|Add new container definition in [docker-compose.yml](../docker-compose.yml) file|Make sure to use a port within the range `5000-5050`. Check which ports are already in use.|

