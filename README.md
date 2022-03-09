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

> :bangbang: Ensure your input data has the expected format.
> For more details, read the [Input Data](docs/architecture.md#input-data) section.

The application waits on your input data.

There are two ways to enter your data and start a [workflow](docs/glossary.md#workflow):
1. CLI shell
2. Imports UI

At the end of the execution, you can collect the enriched data at:
* ./data/exports/
* [Kibana Dashboard](http://localhost:5601)

### CLI Shell

We assume that your shell is in the project root directory.

```shell
./process_zipfile.sh <fullpath-to-zipfile>
```

> :information_source: For additional details on the steps executed,
> check the [Run a DAG](airflow/README.md#run-a-dag) section.

### Imports UI

> :warning: Currently not unavailable.

## Documentation Extra

For further documentation resources, check the _docs_ directory
* [Architecture](docs/architecture.md)
* [Background](docs/background.md)
* [Dev Notes](docs/architecture.md)
* [Glossary](docs/architecture.md)

## Credits

* [stackoverflow.com](http://stackoverflow.com)
* [towardsdatascience.com](https://towardsdatascience.com)
* [medium.com](https://medium.com)

## Licence

[European Union Public Licence (EUPL) V1.2](LICENCE)

