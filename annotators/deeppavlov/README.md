# DeepPavlov API

Python:3.7-slim based Docker image provides a REST API to
call the DeepPavlov Named Entity Recongnition AI framework.
It is an external plugin to tag input texts.

Sources:
* [GitHub](https://github.com/deepmipt/stand_kubernetes_cluster/tree/master/utils/dp_base)
* [DeepPavlov](http://docs.deeppavlov.ai)
  * [ner_ontonotes_bert_mult](https://github.com/deepmipt/DeepPavlov/blob/0.17.1/deeppavlov/configs/ner/ner_ontonotes_bert_mult.json)

## Installation and Usage

![Python](https://img.shields.io/badge/Python-3.7-information)&nbsp;&nbsp;![DeepPavlov](https://img.shields.io/badge/DeepPavlov-0.15.0-information)&nbsp;&nbsp;![Flask](https://img.shields.io/badge/Flask-2.0.1-information)&nbsp;&nbsp;![Flask-RESTful](https://img.shields.io/static/v1?label=Flask%20RESTful&message=0.3.9&color=information)&nbsp;&nbsp;![TensorFlow](https://img.shields.io/badge/TensorFlow-1.15.2-information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build annotators-deeppavlov
```

### Run

```shell
docker-compose up annotators-deeppavlov
```

### API

Send a REST HTTP POST request to the API

> :information_source: The container's port is randomly assigned to enable scaling.
> Run `docker-compose ps` to find the port number

```shell
curl -X POST http://localhost:<port>/model/annotate \
  -H 'Content-Type: application/json' \
  -d '{"texts": ["Un texte d`information sur Rio de Janeiro, écrit à Paris."]}'
```

Test the API

```shell
curl http://localhost:<port>/model/test

# Response: {"test": "passed"}
```

## Develop

```shell
docker-compose run --rm \
  -v smdrm_deeppavlov-volume:/home/deeppavlov/.deeppavlov \
  -v $(pwd)/annotators/deeppavlov:/home/deeppavlov \
  annotators-deeppavlov \
  /bin/bash
```

## Tests

WIP

