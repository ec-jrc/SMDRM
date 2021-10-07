# FloodsAPI

Docker service based on Python:3.8-slim image.

It uses Machine Learning models trained on text related to flood disasters to annotate new incoming texts.
It requires `lang` and `text` fields to be able to compute an annotation.

Batch annotations are supported, and can be controlled with the `BATCH_SIZE_ANNOTATE` environment
variable either via the Engine service or the global .env file.

```shell
curl -v -X POST http://localhost:5001 \
  -H "Content-Type: application/json" \
  -d '{"batch":[{"lang":"en", "text":"a flood disaster @related text. #vivo http://lucot.com"}, {"lang":"en", "text":"#hash another flood disaster related text. @Mymy"}]}'
```

This should return the same data being sent enriched with `text_sanitized` and `annotation` fields

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

## Instructions

For more details, check the [Makefile](Makefile).

### Build

```shell
make image
```

### Download

Download models and embeddings

```shell
make download-*
```
