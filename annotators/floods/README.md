# Floods API

[Python:3.8-slim] based Docker image provides a REST API to call pre-trained
Named Entity Recognition Machine Learning annotators.
We used `Floods` disaster related multilingual texts as training data to annotate
new incoming texts.

It requires `lang` and `texts` fields to be able to compute a correct annotation.

Sources:
* [github.com](https://github.com/panc86/production-flask-app-setup)
* [towardsdatascience.com](https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a)
"""

## Requirements

* Python 3.8
  * keras==2.6.0
  * tensorflow==2.6.0
  * laserembeddings==1.1.2
  * https://download.pytorch.org/whl/cpu/torch-1.10.0%2Bcpu-cp38-cp38-linux_x86_64.whl

The Floods annotator uses those libraries as backend for preprocessing purposes.
We install [Torch CPU only wheel](https://download.pytorch.org/whl/torch/) to save resources.

> Tensorflow logs
disabled with `TF_CPP_MIN_LOG_LEVEL`
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed

## Build

```shell
docker-compose build floods
```

## Run

```shell
docker-compose up floods
```

or

```shell
docker run -it --rm \
  --env-file $(pwd)/annotators/floods/.env \
  -p 5001:5001 \
  jrc/floods_base \
  flask run --host=0.0.0.0 --port=5001
```

## Develop

```shell
docker container run --rm -it \
  -p 5001:5001 \
  -v $(pwd)/annotators/floods:/opt/floods \
  -v floods_volume:/opt/floods/models \
  jrc/floods_base \
  /bin/bash
```

## Usage

Test the API with the following synthetic data points

```shell
curl http://localhost:5001/model/test

# Response
# {
#   "test": "passed"
# }
```

> :information_source:
> Note the `texts` key in the payload, and `en` (lang ISO code) in the URL.

```shell
curl X POST http://localhost:5001/model/annotate/en \
  -H "Content-Type: application/json" \
  -d '{"texts": ["a flood disaster text url","another flood disaster text url"]}'

# Response
# {
#   "disaster_type": "floods",
#   "floods_proba": [
#     "0.022930",
#     "0.006453"
#   ]
# }
```

## Tests

Build the [test](Dockerfile) Docker image

```shell
cd annotators/floods && docker build --target test -t floodsapi:test . && cd -
```

### Unit

Run the unit tests

```shell
cd annotators/floods && docker container run --rm -v $(pwd)/models:/app/models floodsapi:test tests/unit && cd -
```

### Integration

Initialize the test instance of the API

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml up --build floods
```

Run the integration tests

```shell
# note the network flag (see docker-compose.tests.yml)
docker container run --rm --network smdrm_tests floodsapi:test tests/integration
```

Clean up

```shell
# executed from the project root directory
docker-compose -f docker-compose.yml -f docker-compose.tests.yml down
```
