# Floods API

[Python:3.8-slim] based Docker image provides a REST API to call pre-trained
Named Entity Recognition Machine Learning annotators.
We used `Floods` disaster related multilingual texts as training data to annotate
new incoming texts.

It requires `lang` and `texts` fields to be able to compute a correct annotation.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![Flask](https://img.shields.io/badge/Flask-2.0.2-information)&nbsp;&nbsp;![Laser](https://img.shields.io/badge/LaserEmbeddings-1.1.2-information)&nbsp;&nbsp;![TensorFlow](https://img.shields.io/badge/Tensorflow-2.6.0-information)&nbsp;&nbsp;![Keras](https://img.shields.io/badge/Keras-2.6.*-information)&nbsp;&nbsp;![Torch](https://img.shields.io/static/v1?label=TorchC%20PU&message=1.10.0&color=information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build annotators-floods
```

### Run

```shell
docker-compose up annotators-floods
```

### API

Send a REST HTTP POST request to the API

Note the `texts` key in the payload, and the `en` (lang ISO code) in the URL.

> :information_source: The container's port is randomly assigned to enable scaling.
> Run `docker-compose ps` to find the port number

```shell
curl http://localhost:<port>/model/annotate/en \
  -H "Content-Type: application/json" \
  -d '{"texts": ["a flood disaster text url","another flood disaster text url"]}'

# Response: ["0.022930","0.006453"]
```

Test the API

```shell
curl http://localhost:<port>/model/test

# Response: "passed"
```

## Develop

```shell
docker-compose run --rm \
  -v smdrm_floods-volume:/home/floods/models \
  -v $(pwd)/annotators/floods:/home/floods \
  annotators-floods \
  /bin/bash
```

## Tests

Run the unittests

```shell
docker-compose run --rm annotators-floods tests/unit
```

Run the integration tests

WIP

## Credits

* [github.com/angeuwase/production-flask-app-setup](https://github.com/angeuwase/production-flask-app-setup)
* [towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery](https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a)

