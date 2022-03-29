# Social Media Disaster Risk Monitoring

Social Media Disaster Risk Monitoring, *SMDRM* in short, is a Python based data
pipeline application to process social media [_datapoints_](docs/glossary.md#datapoint).

The goal of SMDRM is to provide you with an enriched version of your input data
that you can further analyse, and visualize through a powerful dashboard.

## Installation and Usage

![Docker](https://img.shields.io/badge/Docker-20.10.9-information)&nbsp;&nbsp;![Docker-compose](https://img.shields.io/static/v1?label=Docker%20Compose&message=1.29.1&color=information)&nbsp;&nbsp;![Python](https://img.shields.io/static/v1?label=Python&message=>3.7%20<3.9&color=information)&nbsp;&nbsp;![Code Format](https://img.shields.io/static/v1?label=Code%20Formatter&message=Black&color=information)

> :bangbang: Execute all bash commands from project root directory

### Build

Build the application components

> :coffee: Building the app for the first time can take several minutes to complete

```shell
docker-compose --profile pipelines build
```

### Run

Start the application

> :coffee: Although the command exits successfully,
> the app still takes several minutes to be up and running.

```shell
docker-compose up
```

## Usage

> :bangbang: Ensure your input data has the expected format, and it does not exceed **64mb after compression**.
> For more details, read the [Input Data](docs/architecture.md#input-data) section.

The application waits on you to upload your zipfile data, and start an Airflow [workflow](docs/glossary.md#workflow).

Go to the [SMDRM API](http://localhost:7000/api/v1) swagger UI, and select the uploads/upload endpoint to upload a zipfile.

> :bangbang: Leave the default values for the `dag_id`, and `collection_id` fields.

A response with `{"status": "queued"}` in the payload indicates that Airflow has received the request,
and it has triggered a workflow to processing you input zipfile.

You can check the status of the workflow progress. Go to the [Airflow UI](http://localhost:8080), and click on the Twitter DAG.

Once the workflow is successful, you can use the [Kibana Dashboard](http://localhost:5601) to interactively visualize your enriched data.

## Extras

For further documentation resources, check the _docs_ directory
* [Architecture](docs/architecture.md)
* [Background](docs/background.md)
* [Dev Notes](docs/architecture.md)
* [Glossary](docs/architecture.md)

## Credits

* [stackoverflow.com](http://stackoverflow.com)
* [towardsdatascience.com](https://towardsdatascience.com)
* [medium.com](https://medium.com)
* [freecodecamp.org](https://www.freecodecamp.org/)

## Licence

[European Union Public Licence (EUPL) V1.2](LICENCE)

