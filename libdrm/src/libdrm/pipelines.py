# -*- coding: utf-8 -*-

"""
The Pipes and Filters architectural pattern provides a structure for systems that process a stream of data.
Each processing step is encapsulated in a filter component. Data is passed through pipes between adjacent filters.
Recombining filters allow you to build families of related systems.
"""

import json
import os
import typing
import zipfile

from .datamodels import (
    upload,
    disaster,
    schemas,
)
from .nicelogging import (
    console_logger,
)


console = console_logger("libdrm.pipelines", level="DEBUG")


def pipe_and_filter(start_generator: typing.Iterable, filters: typing.Iterable) -> typing.Iterable:
    generator = start_generator
    for _filter in filters:
        generator = _filter(generator)
    return generator


def iter_zipfile_filter(zip_files: typing.Iterable) -> typing.Iterable[zipfile.ZipExtFile]:
    # iter files from a passed iterator
    # e.g. a glob("*.file_ext") generator
    for zip_file in zip_files:
        # no need to validate as this generator reads zip files
        # that have already passed the validation
        console.debug("processing {}".format(zip_file))
        # iter_content() method iterate JSON files as ZipExtFile objects from the
        # zip file to the next filter in the processing pipeline: iter_json_filter()
        yield from upload.ZipFileModel(zip_file).iter_content()


def iter_jsonfile_filter(json_files: typing.Iterable[zipfile.ZipExtFile]) -> typing.Iterable[bytes]:
    # Receive ZipExtFile based JSON files and iter bytes content.
    # Bytes are validated and objectified in the next step: iter_datapoint_filter()
    for json_file in json_files:
        yield from json_file


def iter_valid_jsondata_filter(bytes_lines: typing.Iterable[bytes]) -> typing.Iterable[dict]:
    # Receive bytes rows from the JSON file and iter OO disaster data points.
    # Data point objects text is prepared in the next step: iter_annotation_filter()
    for bytes_line in bytes_lines:
        is_valid = disaster.DisasterModel.is_valid_json(bytes_line)
        if is_valid is False:
            console.warning("Invalid JSON data found. Skipping {}".format(bytes_line))
            continue
        # filter well formatted JSON bytes only
        yield json.loads(bytes_line)


def iter_datapoints_filter(json_lines: typing.Iterable[dict]) -> typing.Iterable[disaster.DisasterModel]:
    for json_line in json_lines:
        # apply schema validation to detect errors
        errors = schemas.DisasterSchema().validate(json_line)
        # disaster_type field validation error may occur
        if "disaster_type" in errors:
            console.warning(errors)
            # add disaster type from global env
            json_line["disaster_type"] = os.environ["DISASTER_TYPE"]
        data_point = disaster.DisasterModel.schema_serialize_from_dict(json_line)
        yield data_point


def iter_annotation_filter(data_points: typing.Iterable[disaster.DisasterModel]) -> typing.Iterable[disaster.DisasterModel]:
    for data_point in data_points:
        # make API call (assuming the endpoints are up and running)
        # include batch annotate
        yield data_point    # annotated


# zip file processing pipeline steps for each data point (i.e. disaster event)
processing_steps = [
    iter_zipfile_filter,
    iter_jsonfile_filter,
    iter_valid_jsondata_filter,
    iter_datapoints_filter,
    iter_annotation_filter,
]
