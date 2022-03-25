# SMDRM API

Allows the end-user to interacts with the SMDRM components.

## Components

* Airflow: pipelines management
* PowerTrack: data extraction query generation
* UI: user interface to manage collections (i.e. PowerTrack queries)

## Installation and Usage

[Flask-RestX](https://img.shields.io/static/v1?label=Flask-RESTX&message=0.5.1&color=information)&nbsp;&nbsp;![Requests](https://img.shields.io/static/v1?label=Requests&message=2.27.1&color=information)&nbsp;&nbsp;![Pytest](https://img.shields.io/static/v1?label=Pytest&message=7.1.1&color=information)

> :bangbang: Execute all bash commands from project root directory

### Build

```shell
docker-compose build api
```

### Run

```shell
docker-compose up api
```

## Swagger

Go to the [Swagger UI](http://localhost:7000/api/v1) to test the API.

## Configuration

Add a configuration file for a specific environment into the instance directory.
It overrides the default (dev) configuration at application start up.

## Development

```shell
docker-compose run --rm \
    -v $(pwd)/api:/api \
    -v smdrm_uploads-volume:/api/instance/uploads \
    api \
    /bin/bash
```

## Tests

Run the unittests

```shell
docker-compose run --rm api pytest tests/unit
```

Run the integration tests

WIP

