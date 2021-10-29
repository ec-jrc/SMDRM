# Social Media Disaster Risk Monitoring

Social Media Disaster Risk Monitoring, *SMDRM* in short, is a Docker based microservice application.
It supports you to [_prepare_](#prepare), [_annotate_](#annotate), and [_analyse_](#analyse)
[_disaster_](#disaster) related social media [_data points_](#input-data).

You can upload unprocessed compressed data and obtain a new product that can be extracted, monitored,
and/or visualized through a powerful dashboard.

> :information_source: For more info on the jargon used, check the [Glossary](#glossary) section below.

## Architecture

![smdrm_diagram](docs/smdrm-diagram.drawio.png)

*SMDRM Diagram*

Source [diagrams.net](https://www.diagrams.net/)

Table 1 shows the microservices the SMDRM application is made of

|Name|Image|Host|Port|Responsibilities|
|----|-----|----|----|----------------|
|[Upload API](upload/README.md)|[_uploadapi_](build/Dockerfile)|`upload`|`5000`|Validates and caches uploaded zip files to the _uploads_ Docker Volume for other services to use it. Communicates with the Engine API when a file upload terminates|
|[Engine API](engine/README.md)|[_engineapi_](build/Dockerfile)|`engine`|`5555`|Implements a data processing pipeline and contacts the Annotations and ElasticSearch APIs to enrich and save data points|
|[Fires API](annotators/fires/README.md)|[_firesapi_](annotators/fires/Dockerfile)|`fires`|`5002`|Implements Fires disaster type annotation|
|[Floods API](annotators/floods/README.md)|[_floodsapi_](annotators/floods/Dockerfile)|`floods`|`5001`|Implements Floods disaster type annotation|
|ElasticSearch|[_elasticsearch_](docker-compose.yml)|`elasticsearch`|`9200`|Implements ElasticSearch DB for caching enriched data points|
|Kibana|[_kibana_](docker-compose.yml)|`kibana`|`5601`|Implements Kibana UI for visualization and aggregation of enriched data points cached in ElasticSearch DB|

_Table 1. SMDRM Microservices_


## Requirements

### Technology Stack

* Python >3.7,<3.9
* Docker Engine 20.10.9
* Docker Compose 1.29.1, build c34c88b2
* ElasticSearch (DB) & Kibana (UI) 7.15.0
* [Machine Learning NER Algorithms](annotators/README.md)


### Input Data

Table 2 shows the required fields and expected format of the input data

|Field|Type|Format|Description|Note|
|-----|----|------|-----------|----|
|`id`|int| |The unique identifier of a data point|A string number will be converted to integer|
|`created_at`|str|`EEE LLL dd HH:mm:ss Z yyyy`|The date and time at which the data point is created|Twitter based datetime format. Elasticsearch will convert this field to a date provided that it comes in this format. Therefore, make sure you convert your equivalent `created_at` field accordingly.|
|`lang`|str|2 character language code|`en`=English|Any language beside `en`, `es`, `de`, `fr`, `it`, `ar`, `ja`, and `pt` will be converted to `ml` (multilingual) and vectorized with Laserembeddings. For more info, check the Annotators [README.md](annotators/README.md)|
|`text`|str| |The textual information to be annotated and/or geo located|Only textual information that fall inside this field will be considered. Therefore, make sure you sanitize your data accordingly.|
|`annotations`|List[dict]|`{"annotations": [{"annotation_type": "string", "annotation_prob": "float", "sanitized_text": "string"}]`|The JSON response of the annotators used on the data point|Optional field. Populated by selected annotators|
|`latitude`|float| |The place geographic latitude the data point refers to|Optional field|
|`longitude`|float| |The place geographic longitude the data point refers to|Optional field|
|`place_name`|str| |The place name the data point refers to|Optional field|
|`place_type`|str| |The place type the data point refers to|Optional field|

_Table 2. Input Data_

> :information_source: For detailed info about the data model,
> check the [DisasterModel](libdrm/src/libdrm/pipeline.py)


## Usage

This section describes how users should interact with the SMDRM service.

> :information_source: Execute the following commands from the project root directory

The `libdrm` package contains the core functionalities that Docker Containers import to execute specific tasks.
For more info, check the [README.md](libdrm/README.md)


### Build & Run

> :warning: This task required [Docker Engine](https://docs.docker.com/get-docker/),
> and [Docker Compose](https://docs.docker.com/compose/install/) to be installed on you host.

The following command uses [docker-compose.yml](docker-compose.yml) and [.env](.env) files under the hood to define
configurations and environment variables, respectively.

```shell
docker-compose up --build
```

The flag `--build` will ensure all images are built.

> :information_source: Check the status of your service instance with `docker-compose ps`,
> access logs of specific container with `docker-compose logs <container-name>`


### Upload Zip Files

You can upload zip files using the [Upload API](upload/README.md).

> :information_source: You can verify that data points are added to ElasticSearch with
> [http://localhost:9200/_cat/indices?v](http://localhost:9200/_cat/indices?v)
> Look for `docs.counts` for `smdrm-*` index.


### UI

Once the services are up and running, you can access the [Kibana UI](http://localhost:5601).

> :information_source: If you run the SMDRM service locally, the UI is available at you localhost on port 5601.

If you access the UI for the first time, an index pattern needs to be created. Here is how:

* Go to [Kibana](http://localhost:5601)
* Create an [index pattern](http://localhost:5601/app/management/kibana/indexPatterns)
    * add _Name_: `smdrm-*`
    * select _Timestamp Field_: `created_at`
* Go to [Kibana Discover](http://localhost:5601/app/discover)
* Select the data timeframe with the time selector
* Make your custom dashboard


### Development

Use the [development environment](dev/README.md) to create and test new features in a repeatable and standard manner.

### Test

Enter in the [development environment](dev/README.md) and run the tests as follows
```shell
python -m pytest --disable-warnings build/libdrm
```


### Clean Up

Execute the following command to stop the service
```shell
docker-compose down
```

Add the flag `-v` to remove any Docker Volume configured in the [docker-compose.yml](docker-compose.yml) file.

> :warning: Be aware that once you run this command with `-v` the data in ElasticSearch will be deleted,
> and you need to reprocess the zip files again.


## Credits

[SMDRM Diagram](#architecture) thanks to [diagrams.net](https://www.diagrams.net/)


## Glossary

Let us establish a concise glossary of terms that will be the jargon used throughout the documentation.


### Analyse

A SMDRM analysis aim to study the occurrence of an environmental disaster through its location and impact using social
media data points. Data points are enriched with a probability score, and a geographic location that are
extracted from textual information using Machine Learning Named Entity Recognition (NER) algorithms.


### Annotate

The action of assigning a disaster related probability score i.e., a float number between 0 and 1, to the `text` field
in a data point inside.


### Data Point

The smallest data unit. It is a JSON formatted dictionary made of a number of required fields.
For more info, see the [Input Data](#input-data) section.


### Disaster

Within the context of SMDRM, a (environmental) disaster can be of the following types:
* Floods


### Prepare

The action of preparing a set of data points uploaded with a compressed zip file.
It is a data processing pipeline that every zip file go through to validate, clean, annotate, and save its content.


### Uploads

The compressed input data that users intend to enrich.
Each upload has the following requirements:
* at least 1 zip file
* at least 1 JSON file in the zip file
* only 1 JSON formatted data point for each line in the JSON file

You can verify the required data point structure in the [Input Data](#input-data) section.
