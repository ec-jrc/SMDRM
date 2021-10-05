# -*- coding: utf-8 -*-

"""
The Pipes and Filters architectural pattern provides a structure for systems that process a stream of data.
Each processing step is encapsulated in a filter component. Data is passed through pipes between adjacent filters.
Recombining filters allow you to build families of related systems.
"""

import json
import os
import pathlib
import requests
import typing
import zipfile

from libdrm import (
    datamodels,
    nicelogging,
)

console = nicelogging.console_logger("libdrm.pipelines")

# get env variables
batch_size_annotate = int(os.getenv("BATCH_SIZE_ANNOTATE", 100))
# data schema
disaster_schema = datamodels.disaster.DisasterSchema()


def pipe_and_filter(
    start_generator: typing.Iterable, filters: typing.Iterable
) -> typing.Iterable:
    generator = start_generator
    for _filter in filters:
        generator = _filter(generator)
    return generator


def iter_zip_files(
    zip_files: typing.Iterable[pathlib.Path],
) -> typing.Iterable[pathlib.Path]:
    # iter files from a passed iterator
    # e.g. a glob("*.file_ext") generator
    # init zip file schema validation
    schema = datamodels.upload.ZipFileUploadSchema()
    for zip_file in zip_files:
        # validate uploaded zip file via the schema
        # applied is_valid_file() and has_valid_content() func
        errors = schema.validate({"zip_file": zip_file})
        if errors:
            console.warning(errors)
            continue
        yield zip_file


def iter_zip_file_content(
    zip_files: typing.Iterable[pathlib.Path],
) -> typing.Iterable[zipfile.ZipExtFile]:
    # only valid zip files that passed schema validation
    for zip_file in zip_files:
        # iter_content() method iterate JSON files as ZipExtFile objects from the
        # zip file to the next filter in the processing pipeline
        for _file in datamodels.upload.iter_content(zip_file):
            yield _file


def iter_json_file_content(
    json_files: typing.Iterable[zipfile.ZipExtFile],
) -> typing.Iterable[dict]:
    # Receive ZipExtFile based JSON files and yield JSON decoded bytes.
    for json_file in json_files:
        for row in json_file:
            # we can only validate JSON formatted data through the schema
            # Hence, we need to first validate the raw bytes data with an ad hoc try/except method.
            valid = datamodels.disaster.DisasterModel.is_valid_json(row)
            # filter out rows with invalid JSON format
            if not valid:
                console.warning("Invalid JSON data found. Skipping...")
                continue
            # yield as JSON to allow the application of schema validation
            yield json.loads(row)


def iter_disaster_data_points(
    data_points: typing.Iterable[dict],
) -> typing.Iterable[dict]:
    for data_point in data_points:
        # apply schema validation to detect errors
        errors = disaster_schema.validate(data_point)
        # disaster_type field validation error may occur
        if "disaster_type" in errors:
            console.warning(errors)
            # add disaster type from global env
            data_point["disaster_type"] = os.environ["DISASTER_TYPE"]
        yield datamodels.disaster.DisasterModel.schema_serialize_from_dict(
            data_point
        ).deserialize_to_dict()


def call_annotation_api(batch, endpoint=os.getenv("DISASTER_TYPE")):
    # available endpoints
    endpoints = {
        "floods": "http://floods:5001/predict",
        "fires": "http://fires:5002/predict",
    }
    # make API call (assuming the endpoints are up and running)
    return requests.post(endpoints[endpoint], json={"batch": batch})


def iter_batch_annotate(
    data_points: typing.Iterable[dict], batch_size=batch_size_annotate
):
    batch = []
    for data_point in data_points:
        # increase batch size
        batch.append(data_point)
        if len(batch) == batch_size:
            # make API call (assuming the endpoints are up and running)
            response = call_annotation_api(batch)
            # the api response is the annotated data point
            yield response.json()
            # flush batch
            batch = []
        continue


# zip file processing pipeline steps for each data point (i.e. disaster event)
processing_steps = [
    iter_zip_files,
    iter_zip_file_content,
    iter_json_file_content,
    iter_disaster_data_points,
    iter_batch_annotate,
]
