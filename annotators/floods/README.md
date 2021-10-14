# FloodsAPI

Docker service based on Python:3.8-slim image.

It uses Machine Learning models trained on text related to flood disasters to annotate new incoming texts.
It requires `lang` and `text` fields to be able to compute an annotation.

You can control the annotation batch size with `BATCH_SIZE_ANNOTATE` environment variable in the Engine .env file.

## Instructions

You need to download models and embeddings, then run the FloodsAPI

> :information_source: The following commands are executed from the project root directory

### Download

```shell
bash build/development.sh
```

Then execute the following command in the shell
```shell
bash annotators/floods/downloads.sh
```

The flag `--clear` deletes any models previously downloaded

### Run

Build and run the FloodsAPI
```shell
docker-compose up --build floods
```

### Test

Test the API with the following synthetic data points

> :information_source: Note the "batch" key in the payload.

```shell
curl -v -X POST http://localhost:5001 \
  -H "Content-Type: application/json" \
  -d '{"batch":[{"lang":"en", "text":"a flood disaster @related text. #vivo http://lucot.com"}, {"lang":"en", "text":"#hash another flood disaster related text. @Mymy"}]}'
```

This should return the same data points being sent, enriched with `text_sanitized` and `annotation` fields

```shell
{
  "batch": [
    {
      "lang": "en",
      "text": "a flood disaster @related text. #vivo http://lucot.com",
      "text_sanitized": "a flood disaster USER text vivo URL",
      "annotation": "0.00017365074"
    },
    {
      "lang": "en",
      "text": "#hash another flood disaster related text. @Mymy",
      "text_sanitized": "hash another flood disaster related text USER",
      "annotation": "0.009030139"
    }
  ]
}
```
