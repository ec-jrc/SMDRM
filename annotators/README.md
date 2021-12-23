# Annotators

The Machine Learning models to annotate the textual information in the disaster related data points.
Each model is available by means of HTTP API call to a dedicated endpoint.

## Endpoints

The API endpoint format is `http://<host>:<port>/<resource>`
The `port` ranges for annotators is `5001-5050`. This means a total of `50` annotator APIs can be run in parallel.
The `host` variable depends on the location where an HTTP call is executed.
Within the Docker environment, `host` is the Docker _container name_ of the service you are calling. Whereas, `host` is
`localhost` (or `127.0.0.1`) when in running locally from your host machine.

For example, you can use the following endpoints to call the Floods Annotator API:
* `http://floods:5001/annotate` from another Docker container
* `http://localhost:5001/annotate` from your host machine

## Available Annotators

At the moment, `Floods` annotator algorithm is publicly available for download, and usage under the
[European Union Public Licence V. 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12) license.

There are few algorithms under testing that will be released soon.
These are:
* Fires
* ImageClassification

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
|5|Add new container definition in [docker-compose.yml](../docker-compose.yml) file|Make sure to use a port within the range `5001-5050`. Check which ports are already in use.|

## Performance Tests

Performance tests are run against the test dataset of choice.
To run a performance test you first need to:
* build the [test image](tests/Dockerfile)
* initiate the Annotator APIs to run the test against
* run the test against a specific API

> :information_source: Execute the following command from the project root directory

### Build Test Image

```shell
docker build -t annotators-perftests:v1 annotators/tests/
```

### Initiate Annotator

Use `docker-compose.tests.yml` to spin a new set of containers with test specific
port mapping.

```shell
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build floods
```

### Run Tests

When the API is ready, you can trigger the performance tests for a specific
annotator by passing its URL as argument of the Docker `CMD`.

For instance, let's run the performance test for Floods API using the default data
```shell
# floods-test is the container name where the API is available
docker container run --rm -it \
  --network smdrm_tests \
  annotators-perftests:v1 \
  --annotator-url http://floods-test:15001
```

## Troubleshooting

> :warning: WARNING :warning:
> Given the size of some Machine Learning packages, you might incur in the
> Out Of Memory (OOM) error on Mac and Windows OS.
> You must allocate at least 4 GB of memory to containers to avoid that.
> For more info, check the Resource management pages for your OS:
> * [Mac](https://docs.docker.com/desktop/mac/#resources)
> * [Windows](https://docs.docker.com/desktop/windows/#resources)
