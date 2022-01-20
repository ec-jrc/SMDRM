# [DeepPavlov](http://docs.deeppavlov.ai/en/master/index.html) API

A REST API instance of the DeepPavlov Named Entity Recongnition
AI framework. It is an external plugin to tag input texts.

A dockerized version is also available on
[Docker Hub](https://hub.docker.com/r/deeppavlov/base-cpu).

For more details, check the
[Integrations](http://docs.deeppavlov.ai/en/master/integrations/rest_api.html)
section in the Official Documentation, and the
[GitHub](https://github.com/deepmipt/stand_kubernetes_cluster/tree/master/utils/dp_base)
page.

## Swagger

Access the Swagger Docs @ http://localhost:5000

## Requirements

* Docker ~= 20
* docker-compose
* [ner_ontonotes_bert_mult](https://github.com/deepmipt/DeepPavlov/blob/0.17.1/deeppavlov/configs/ner/ner_ontonotes_bert_mult.json)

> :bangbang: execute all bash commands from project root directory

## Build

Export `ENV` varible to build the image for that environment 

```shell
./build_task.sh annotators/deeppavlov
```

## Run

```shell
docker-compose up -d deeppavlov
```

or as an isolated service for development purpose

```shell
docker container run --rm -it \
  --env-file $(pwd)/annotators/deeppavlov/.env \
  -v smdrm_deeppavlov:/opt/deeppavlov/.deeppavlov \
  smdrm/annotators/deeppavlov \
  bash
```

## Usage

```shell
curl -X POST http://localhost:5000/model \
  -H 'Content-Type: application/json' \
  -d '{"texts": ["Un texte d`information sur Rio de Janeiro, écrit à Paris."]}'
```

## Tests

```shell
curl -X POST http://localhost:5000/test
```

Should return `"passed"` if REST API service is healthy, or `"failed"`.

