# Floods API

[Python:3.8-slim] based Docker image provides a REST API to call pre-trained
Named Entity Recognition Machine Learning annotators.
We used `Floods` disaster related multilingual texts as training data to annotate
new incoming texts.

It requires `lang` and `texts` fields to be able to compute a correct annotation.

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.8-information)&nbsp;&nbsp;![Flask](https://img.shields.io/badge/Flask-2.0.2-information)&nbsp;&nbsp;![Laser](https://img.shields.io/badge/LaserEmbeddings-1.1.2-information)&nbsp;&nbsp;![Torch](https://img.shields.io/static/v1?label=TorchC%20PU&message=1.10.0&color=information)

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

> :information_source: Note the `texts` key in the payload,
> and `en` (lang ISO code) in the URL.

```shell
# from host network
curl http://localhost:5010/model/annotate/en \
  -H "Content-Type: application/json" \
  -d '{"texts": ["a flood disaster text url","another flood disaster text url"]}'

# Response: ["0.022930","0.006453"]
```

Test the API

```shell
curl http://localhost:5010/model/test

# Response: "passed"
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

## Tests

Build the Docker image for testing

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

## Credits

* [github.com/angeuwase/production-flask-app-setup](https://github.com/angeuwase/production-flask-app-setup)
* [towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery](https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a)

