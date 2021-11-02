# Fires API

> :bangbang: **IMPORTANT NOTICE**
> 
> Currently, this annotator is under internal evaluation, and it has not had made available to the public yet.
> We will release it soon together with an official publication.
> 
> If you would like to use it before the official release,
> please contact [Valerio Lorini](mailto:valerio.lorini@ec.europa.eu?subject=[SMDRM]%20Fires%20Annotator%20Access).

Docker service based on `Python:3.8-slim` image.

It uses Machine Learning models trained on text related to fire disasters to annotate new incoming texts.
It requires `text` (the raw textual information to be annotated),
and `annotations` (the placeholder list to store annotation results) fields to be able to compute an annotation.

> :information_source: You can control the annotation batch size with the `ANNOTATION_BATCH_SIZE`
> environment variable in the Engine .env file.

## Requisites

* Docker >= 19
* Python 3.8
  * [pip dependencies](requirements.txt)

## Instructions

You need to download the model, then run the Fires API

> :information_source: The following commands are executed from the project root directory

### Download

Use this [download link](https://drive.google.com/drive/folders/1QBiJG73kwinsuE0Lr2pqN5WeMnegKhG9?usp=sharing) to
get the model binary files from the hosting cloud provider.

Ensure the following filesystem structure in the root level of the _models_ directory

```shell
# folder structure
fires/
  ...
  models/
    config.json
    optimizer.pt
    pytorch_model.bin
    scheduler.pt
    trainer_state.json
    trainer_args.bin
```

### Run

Build and run the FloodsAPI
```shell
docker-compose up --build fires
```

### Tests

Test the API with the following synthetic data points

> :information_source: Note the `batch` and `annotations` fields in the payload.

```shell
curl -v -X POST http://localhost:5002 \
  -H "Content-Type: application/json" \
  -d '{"batch":[{"annotations":[], "text":"a fires disaster @related text. #vivo http://lucot.com"}, {"annotations":[], "text":"#hash another wild fire disaster related text. @Mymy"}]}'
```

This should return the batch, enriched with the annotations

```shell
{
  "batch": [
    {
      "annotations": [
        {
          "annotation_type": "fires",
          "annotation_prob": 0.9998450215352932,
          "sanitized_text": "a fires disaster USER text vivo URL"
        }
      ],
      "text": "a fires disaster @related text. #vivo http://lucot.com"
    },
    {
      "annotations": [
        {
          "annotation_type": "fires",
          "annotation_prob": 0.8669703006744385,
          "sanitized_text": "hash another wild fire disaster related text USER"
        }
      ],
      "text": "#hash another wild fire disaster related text. @Mymy"
    }
  ]
}
```
