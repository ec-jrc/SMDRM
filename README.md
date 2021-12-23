# Social Media Disaster Risk Monitoring

Social Media Disaster Risk Monitoring, *SMDRM* in short, is a dockerized ETL pipeline.
It helps you to [_prepare_](#prepare), [_annotate_](#annotate), and [_analyse_](#analyse)
[_disaster_](#disaster) related social media [_datapoints_](#input-data-model).

You can upload unprocessed compressed data and obtain a new product that can be extracted, monitored,
and/or visualized through a powerful dashboard.

> :information_source: For more info on the jargon used, check the [Glossary](#glossary) section below.

The SMDRM ETL pipeline is made of a set of sequential _tasks_.
For each task there will be:
* a *.zip formatted input
* a data processing logic
* a *.zip formatted output

## Architecture

Table 1 shows the tasks the SMDRM ETL pipeline is built upon

COMING SOON

|Name|Image|Command|Description|
|----|-----|-------|-----------|
|Extract_tweets| | | |
|Transform_tweets| | | |

_Table 1. SMDRM Data Processing Tasks_

Table 2 shows the external plugins the SMDRM ETL pipeline uses to enrich the input datapoints

|Name|Image|Host|Port|Responsibilities|
|----|-----|----|----|----------------|
|[Floods API](annotators/floods/README.md)|[_floodsapi_](annotators/floods/Dockerfile)|`floods`|`5001`|Implements Floods disaster type annotation|

_Table 2. External Plugins_

## Requirements

### Tech Stack

* Python >3.6,<3.10
* Docker Engine 20.10.9
* Docker Compose 1.29.1, build c34c88b2
* Airflow 2.2.2
* ElasticSearch (DB) & Kibana (UI) 7.15.0
* [Machine Learning NER Algorithms](annotators/README.md)


### Input Data Model

Table 2 shows the _required_ fields and expected format of the input data

|Field|Type|Format|Description|Note|
|-----|----|------|-----------|----|
|`id`|int| |The unique identifier of a datapoint|A string number will be converted to integer|
|`created_at`|str|`EEE LLL dd HH:mm:ss Z yyyy`|The date and time at which the datapoint is created|Twitter based datetime format. Elasticsearch will convert this field to a date provided that it comes in this format. Therefore, make sure you convert your equivalent `created_at` field accordingly.|
|`lang`|str|2 character language code|`en`=English|Any language beside `en`, `es`, `de`, `fr`, `it`, `ar`, `ja`, and `pt` will be converted to `ml` (multilingual) and vectorized with Laserembeddings. For more info, check the Annotators [README.md](annotators/README.md)|
|`text`|str| |The textual information to be annotated and/or geo located|Only textual information that fall inside this field will be considered. Therefore, make sure you sanitize your data accordingly.|

_Table 2. Input Data Model_

The input data, including all required fields, can also be wrapped inside a `tweet` field.
This is an _ad hoc_ method to ingest data from a legacy product that structured it that way.

## Credits

## Glossary

Let us establish a concise glossary of terms that will be the jargon used throughout the documentation.

### Analyse

A SMDRM analysis aim to study the occurrence of an environmental disaster through its location and impact using social
media datapoints. Datapoints are enriched with a probability score, and a geographic location that are
extracted from textual information using Machine Learning Named Entity Recognition (NER) algorithms.

### Annotate

The action of assigning a probability score to the `text` field of a datapoint
i.e., a float number between 0 and 1 representing the likelihood that the textual
information in the `text` field refers to a specific disaster type.

### Datapoints

The smallest data unit. It is a JSON formatted dictionary made of a number of required fields.
For more info, see the [Input Data Model](#input-data-model) section.

### Disaster

Within the context of SMDRM, a (environmental) disaster can be of the following types:
* Floods

### Prepare

Prepare a zip file of datapoints means:
* extract valid rows as well as required fields, and
* transform extracted rows to be ready for annotation

### Uploads

The compressed input data that users intend to enrich.
Each upload has the following requirements:
* at least 1 zip file
* at least 1 JSON file in the zip file
* only 1 JSON formatted datapoint for each line in the JSON file

You can verify the required datapoint structure in the [Input Data Model](#input-data-model) section.
