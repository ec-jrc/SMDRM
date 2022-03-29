# Developer's Note

Notes on current and future development.

## Annotator Endpoint Format

The API endpoint format is `http://<host>:<port>/model/annotate`
The `host` variable is the annotator ID.
The default `port` for communication between containers inside the Docker network is 5000.
A random port is opened to allow the host machine (where the Docker service is running) to connect to the container.

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
|5|Add new container definition in [docker-compose.yml](../docker-compose.yml) file|Make sure to set the internal port to 5000.|

