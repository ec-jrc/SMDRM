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

> :bulb: TIP: Tensorflow logs are disabled with `TF_CPP_MIN_LOG_LEVEL=x`
> * 0 = all messages are logged (default behavior)
> * 1 = INFO messages are not printed
> * 2 = INFO and WARNING messages are not printed
> * 3 = INFO, WARNING, and ERROR messages are not printed

> :bangbang: execute all bash commands from project root directory

## Build

```shell
docker-compose build annotators-floods
```

## Run

```shell
docker-compose up annotators-floods
```

## Develop

```shell
export FLASK_ENV=development
docker-compose run --rm \
  -v smdrm_floods:/opt/floods/models \
  -v $(pwd)/annotators/floods:/opt/floods \
  annotators-floods \
  /bin/bash
```

## API

### Usage

```shell
# from host network
curl http://localhost:5010/model/annotate/en \
  -H "Content-Type: application/json" \
  -d '{"texts": ["a flood disaster text url","another flood disaster text url"]}'

# Response
# ["0.022930","0.006453"]
```

### Test

Test the API with the following synthetic data points

```shell
# from host network
curl http://localhost:5010/model/test

# Response
# "passed"
```

> :information_source:
> Note the `texts` key in the payload, and `en` (lang ISO code) in the URL.
Build the Docker image for testing


## Tests

Build the Docker image for tests

```shell
export ENV=test
docker-compose build annotators-floods
```

### Unit

Run the unit tests

```shell
docker-compose run --rm annotators-floods tests/unit
```

### Integration

WIP

