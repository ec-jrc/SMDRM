# -*- coding: utf-8 -*-

"""
The Pipes and Filters architectural pattern provides a structure for systems that process a stream of data.
Each processing step is encapsulated in a filter component. Data is passed through pipes between adjacent filters.
Recombining filters allow you to build families of related systems.
"""

import json
import pathlib
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


def iter_jsonfile_filter(json_files: typing.Iterable) -> typing.Iterable[bytes]:
    # Receive ZipExtFile based JSON files and iter bytes content.
    # Bytes are validated and objectified in the next step: iter_datapoint_filter()
    for json_file in json_files:
        yield from json_file


def iter_datapoint_filter(json_file: typing.Iterable) -> disaster.DisasterModel:
    # Receive bytes rows from the JSON file and iter OO disaster data points.
    # Data point objects text is prepared in the next step: iter_annotation_filter()
    for brow in json_file:
        valid = disaster.DisasterModel.validate_json(brow)
        if not valid:
            console.debug("Malformed JSON data: {}".format(brow))
        yield disaster.DisasterModel.from_bytes(brow)


def iter_annotation_filter(data_points: typing.Iterable[disaster.DisasterModel]):
    for data_point in data_points:
        # make API call
        # include batch annotate
        yield data_point    # annotated


#files = pathlib.Path("/home/ep/Downloads/fires").glob("*.zip")

files = [pathlib.Path("/home/ep/Downloads/fires/test_data.zip")]
filters = [iter_zipfile_filter, iter_jsonfile_filter, iter_datapoint_filter, ]
pipeline = pipe_and_filter(files, filters)

for step in pipeline:
    print(step)
