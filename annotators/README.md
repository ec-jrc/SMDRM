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
* [Fires](fires/README.md)
* ImageClassification

## Add a new Annotator API

### Intro

You will create a dedicated [Python based](https://hub.docker.com/_/python) Docker Image for the new API.

> :information_source: We do NOT inherit from the [base image](../build/Dockerfile), but from a community based Python Image for two reasons:
> 1) Machine learning packages depends on different Python versions. Hence, we need freedom to choose a different Python version for any new annotator.
> 2) Usually, machine learning packages are computationally expensive to install. If we use the base image, we would need to rebuild the Docker image of an annotator
every time we change the base image. Therefore, we want to keep the build time fast for development by not having the need to rebuild the expensive Docker images.

### Request IO

An annotation API expects an HTTP POST request with a batch of JSON data points as the data payload with
`{"batch": [{"id": 1}, {"id": 2}, ...]}` format. The API returns the batch of data points annotated with
the annotators chosen at upload time via the [Upload API](../upload/README.md#metadataupload).

This is an example of HTTP POST request/response to the Floods Annotator API (`port=5001`) using cURL.
Note the payload (`-d`) format `{"batch": [{}, {}, ...]}`.

```shell
curl -v -X POST http://localhost:5001 \
  -H "Content-Type: application/json" \
  -d '{"batch":[{"lang":"en", "text":"a flood disaster @related text. #vivo http://lucot.com"}, {"lang":"en", "text":"#hash another flood disaster related text. @Mymy"}]}'
```

```shell
{
  "batch": [
    {
      "lang": "en",
      "text": "a flood disaster @related text. #vivo http://lucot.com",
      "annotations": [
        {
          "annotation_type": "floods",
          "annotation_prob": "0.00017365074",
          "sanitized_text": "a flood disaster USER text vivo URL"
        }
      ]
    },
    {
      "lang": "en",
      "text": "#hash another flood disaster related text. @Mymy",
      "annotations": [
        {
          "annotation_type": "floods",
          "annotation_prob": "0.009030139",
          "sanitized_text": "hash another flood disaster related text USER"
        }
      ]
    }
  ]
}
```

### Steps

Table 1 lists the sequence of steps to implement a new annotator API.

> :information_source: The following steps are executed inside the annotators/ directory.
> Use other annotators as template to build your own annotator.

|Step|Action|Notes|
|---:|------|-----|
|1|Create a new directory `annotators/<newapi>/`| |
|2|Download/Create the trained Machine Learning prediction model into `annotators/<newapi>/models/`| |
|3|Create new api.py file with Flask-RestFul based API| |
|4|Set the instructions to build a new Docker image in a new Dockerfile| |
|5|Add new container definition in [docker-compose.yml](../docker-compose.yml) file|Make sure to use a port within the range `5001-5050`.|
|6|Add new URL endpoint in [`libdrm.apis.APIs_lookup`](../libdrm/src/libdrm/apis.py)|Format: `{"<newapi>_annotator": "http://<newapi>:<port>/<resource>"}`.|
|7|Add metadata field in [`libdrm.schemas.MetadataUploadSchema`](../libdrm/src/libdrm/schemas.py) Marshmallow schema|Format: `<newapi>_annotator=marshmallow.fields.Boolean(load_default=False)`<br>By default, it is set to `False` to keep annotation optional.|

## Performance Tests

Performance tests are run against the test dataset of choice.
To run a performance test you first need to:
* initiate the Annotator APIs to run the test against
* build the [test image](tests/Dockerfile)
* run the test against a specific API

> :information_source: Execute the following command from the project root directory

### Initiate Annotator APIs

```shell
# initialize fires and floods annotators
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build floods fires
```

### Build Test Image

```shell
docker build -t annotators-perftests:v1 annotators/tests/
```

### Run Performance Test

When the APIs are up and running you can trigger the performance tests for a specific API by passing its URL as argument
of the Docker CMD

For instance, let's run the performance test for Floods API using the default data
```shell
# floods-test is the container name where the API is available
docker run --rm -it --network smdrm_tests annotators-perftests:v1 --url "http://floods-test:15001"
```

## Troubleshooting

> :warning: WARNING :warning:
> Given the size of some Machine Learning packages, you might incur in the
> Out Of Memory (OOM) error on Mac and Windows OS.
> You must allocate at least 4 GB of memory to containers to avoid that.
> For more info, check the Resource management pages for your OS:
> * [Mac](https://docs.docker.com/desktop/mac/#resources)
> * [Windows](https://docs.docker.com/desktop/windows/#resources)
