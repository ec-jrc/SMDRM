# DeepPavlov API

[Python:3.7-slim] based Docker image provides a REST API to
call the DeepPavlov Named Entity Recongnition AI framework.
It is an external plugin to tag input texts.

Sources:
* [GitHub](https://github.com/deepmipt/stand_kubernetes_cluster/tree/master/utils/dp_base) page.
* [DeepPavlov](http://docs.deeppavlov.ai)
section in the Official Documentation, and the

## Requirements

* Python 3.7
  * deeppavlov==0.15.0
  * tensorflow==1.15.2
  * [ner_ontonotes_bert_mult](https://github.com/deepmipt/DeepPavlov/blob/0.17.1/deeppavlov/configs/ner/ner_ontonotes_bert_mult.json)

> :bulb: TIP: Tensorflow logs are disabled with `TF_CPP_MIN_LOG_LEVEL=x`
> * 0 = all messages are logged (default behavior)
> * 1 = INFO messages are not printed
> * 2 = INFO and WARNING messages are not printed
> * 3 = INFO, WARNING, and ERROR messages are not printed

> :bangbang: execute all bash commands from project root directory

## Build

```shell
docker-compose build annotators-deeppavlov
```

## Run

```shell
docker-compose up annotators-deeppavlov
```

## Develop

```shell
docker-compose run --rm \
  -v smdrm_deeppavlov:/opt/deeppavlov/.deeppavlov \
  -v $(pwd)/annotators/deeppavlov:/opt/deeppavlov \
  annotators-deeppavlov \
  /bin/bash
```

## API

### Usage

```shell
curl -X POST http://localhost:5000/model \
  -H 'Content-Type: application/json' \
  -d '{"texts": ["Un texte d`information sur Rio de Janeiro, écrit à Paris."]}'
```

### Test

```shell
curl -X POST http://localhost:5000/model/test
```

Should return `"passed"` if REST API service is healthy, or `"failed"`.

## Tests

Build the Docker image for tests

```shell
export ENV=test
docker-compose build annotators-deeppavlov
```

### Unit

WIP

### Integration

WIP

