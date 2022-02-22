# Social Media Disaster Risk Monitoring

Social Media Disaster Risk Monitoring, *SMDRM* in short,
is a Python based data ETL pipeline application to process social media [_datapoints_](#input-data-model).

The goal of SMDRM is to provide you with an enriched version of your input data
that you can further analyse, and visualize through a powerful dashboard.

## Background

SMDRM enables analysis aim to study the occurrence of environmental disasters through its location,
and urban impact using social media datapoints. Datapoints are enriched with a probability score,
and a geographic location that are extracted from datapoint text using Named Entity Recognition (NER) algorithms.

## Requirements

* Python >3.7,<3.9
* Docker Engine 20.10.9
* Docker Compose 1.29.1, build c34c88b2
* Airflow 2.2.3
* ElasticSearch (DB) & Kibana (UI) 7.15.0
* [Machine Learning NER Algorithms](annotators/README.md)

## Build

> :bangbang: Execute all bash commands from project root directory

```shell
docker-compose --profile pipelines build
```

> :coffee: Build for the first time can take several minutes to complete.

## Run

```shell
docker-compose up airflow-init && docker-compose up
```

> :coffee: Although, the command exits successfully, a lot happens behind the scene.
> The service can take several minutes to be up and running.

## Trigger a DAG run

> :bangbang: Before running your first DAG, make sure your input data has the
> expected format. Read the [Input Format](#input-format) section in Architecture.

See [Run a DAG](airflow/README.md#run-a-dag) section.

## Architecture

> :bangbang: Currently, SMDRM is able to process Twitter based datapoints.
> For more details, check the [Twitter Object Model](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet).

The main components of SMDRM are:
* Docker - ensures consistency, reproducibility, and portability across Operating Systems
* NER annotators - recognize and [annotate](docs/glossary.md#annotate) [disaster types](docs/glossary.md#disaster),
  and places information in datapoints
* Apache Airflow - authors, schedules, and monitors [workflows](docs/glossary.md#workflow)
  as [Directed Acyclic Graphs](docs/glossary.md#DAG) (DAGs) of _tasks_ in an automated, and distributed manner.

> :information_source: For more info on the jargon used, check the [Glossary](docs/glossary.md).

### Input Format

The expected input data is a zipfile archive of one, or more NDJSON files.
NDJSON files must be located in the root of the zipfile archive.
Sub-directory file search is not supported.

For example,

```shell
zipinfo -m data/legacy.zip

# Valid ouptut:
# Archive:  data/legacy.zip
# Zip file size: 78385 bytes, number of entries: 1
# ?rw-------  2.0 unx    78271 b-  0% stor 21-Dec-05 15:36 0.ndjson
# 1 file, 78271 bytes uncompressed, 78271 bytes compressed:  0.0%
``` 

### Diagram

Add diagram here

## Twitter DAG

In general, a DAG is a set of sequential _tasks_ i.e., a pipeline.
Each task takes an input, executes a processing logic, and returns an output

> :bangbang: At the moment, only one DAG to process Twitter datapoints is operational: `twitter` DAG

### Tasks

Table 1 shows the Twitter DAG _tasks_

|Name|Description|
|----|-----------|
|`extract_tweets`|Extracts required fields from raw data, and generates new fields to create the Datapoint model.|
|`transform_tweets`|Apply place and grammar normalization transformations to clean the `text` field and identify place candidates.|
|`floods_annotate`|Assign a floods related probability score to the datapoint given its (cleaned) `text`.|
|`geocode_tweets`|Assign latitude and longitude coordinates to the datapoint whose place candidates matches against a [GADM](https://gadm.org) based [Global Places gazettier](geocode_tweets/config/global_places_v1.tsv).|

_Table 1. Twitter DAG Tasks_

## External Plugins

Table 2 shows the external plugins the Twitter DAG uses to enrich the input datapoints

|Name|Image|URL|Responsibilities|
|----|-----|---|----------------|
|[DeepPavlov API](annotators/deeppavlov/README.md)|[_deeppavlov_](annotators/deeppavlov/Dockerfile)|`http://localhost:5000/`|DeepPavlov NER REST API for geo political, location, and facility entity tagging.|
|[Floods API](annotators/floods/README.md)|[_floods_](annotators/floods/Dockerfile)|`http://floods:5010/`|Floods NER REST API to annotate floods disaster type related datapoints.|

_Table 2. External Plugins_

## Input Data Model

Table 2 shows the required fields of the input data.

|Field|Type|Format|Description|Note|
|-----|----|------|-----------|----|
|`id`|int| |The unique identifier of a datapoint|A string number will be converted to integer|
|`created_at`|str|`EEE LLL dd HH:mm:ss Z yyyy`|The date and time at which the datapoint is created|Twitter based datetime format. Elasticsearch will convert this field to a date provided that it comes in this format. Therefore, make sure you convert your equivalent `created_at` field accordingly.|
|`lang`|str|2 character language code|`en`=English|Any language beside `en`, `es`, `de`, `fr`, `it`, `ar`, `ja`, and `pt` will be converted to `ml` (multilingual) and vectorized with Laserembeddings. For more info, check the Annotators [README.md](annotators/README.md)|
|`text`|str| |The textual information to be annotated and/or geo located|Only textual information that fall inside this field will be considered. Therefore, make sure you sanitize your data accordingly.|

_Table 2. Input Data Model_

> :information_source: The input data, including all required fields, can also be wrapped inside a `tweet` field.
> This is an _ad hoc_ method to ingest data from a legacy product that structured it that way.

### Data Enrichment Fields

Table 3 shows the additional fields generated by the Twitter DAG tasks.

|Field|Type|Creator|Users|Description|
|-----|----|-------|-----|-----------|
|`annotation`|dict|`extract_tweets`|`floods_annotate`|Annotation scores placeholder.|
|`annotation.floods`|float| | |Annotation score.|
|`place`|dict|`extract_tweets`|`transform_tweets`,`geocode_tweets`|Geographic attribures placeholder.|
|`place.candidates`|dict|`transform_tweets`|`geocode_tweets`|GPE, FAC, and LOC place candidates returned by DeepPavlov API.|
|`place.coordinates`|list|`geocode_tweets`|`geocode_tweets`|[Latitude, longitude] coordinate list for each place candidate matched against Global Places gazettier.|
|`place.meta`|dict|`geocode_tweets`|`geocode_tweets`|Metadata of place candidates matched against the Global Places gazettier.|
|`place.meta.country_name`|str|`geocode_tweets`|`geocode_tweets`|The name of the Country.|
|`place.meta.country_code`|str|`geocode_tweets`|`geocode_tweets`|The alpha-3 code ISO 3166 Country code.|
|`place.meta.region_name`|str|`geocode_tweets`|`geocode_tweets`|The GADM level 1, or 2 region name.|
|`place.meta.city_name`|str|`geocode_tweets`|`geocode_tweets`|The name of the city. It is populated only when place candidates are matched against the Global Places gazettier.|
|`place.meta.region_id`|str|`geocode_tweets`|`geocode_tweets`|The region identifier. Used internally.|
|`text_clean`|str|`extract_tweets`|`transform_tweets`|Normalized textual information|

_Table 3. Data Enrichment Fields__

## Credits

