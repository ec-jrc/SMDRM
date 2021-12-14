# [DeepPavlov](http://docs.deeppavlov.ai/en/master/index.html) API

A ready-to-use REST API instance of the DeepPavlov Named Entity Recongnition
AI framework. It is an external plugin to tag input texts.
Source [Docker Hub](https://hub.docker.com/r/deeppavlov/base-cpu).

For more details, check the
[Integrations](http://docs.deeppavlov.ai/en/master/integrations/rest_api.html)
section in the Official Documentation, and the
[GitHub](https://github.com/deepmipt/stand_kubernetes_cluster/tree/master/utils/dp_base)
page.

Requires:
* Docker ~= 20
* docker-compose
* [ner_ontonotes_bert_mult](https://github.com/deepmipt/DeepPavlov/blob/0.17.1/deeppavlov/configs/ner/ner_ontonotes_bert_mult.json)

> :bangbang: execute all bash commands from project root directory

## Build

```shell
docker-compose up --build deeppavlov
```

## Usage

```shell
curl -X POST http://127.0.0.1:5000/model \
  -H 'Content-Type: application/json' \
  -d '{"x": ["Un texte d`information sur Rio de Janeiro, écrit à Paris."]}'
```

## Tests

```shell
curl -X 'POST' \
  'http://localhost:5000/probe' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"x": ["test"]}'
```

Should return `["Test passed"]` if REST API service is healthy.


## Swagger

Access the Swagger Docs @ http://localhost:5000
