"""
The Pipes and Filters architectural pattern provides a structure for systems that process a stream of data.
Each processing step is encapsulated in a filter component. Data is passed through pipes between adjacent filters.
Recombining filters allow you to build families of related systems.

Resources:
    - https://betterprogramming.pub/3-data-processing-pipelines-you-can-build-with-python-generators-dc0d2019b177
"""

import collections
import os
import pathlib
import typing
import zipfile

import libdrm.datamodels
import libdrm.deploy
import libdrm.nicelogging


# logging
console = libdrm.nicelogging.console_logger("libdrm.pipeline")
# data schema
disaster_schema = libdrm.datamodels.disaster.DisasterSchema()
upload_file_schema = libdrm.datamodels.upload.ZipFileUploadSchema()


def pipe_and_filter(generator: typing.Iterable, filters: typing.Iterable[typing.Callable]) -> typing.Iterable:
    _generator = generator
    for _filter in filters:
        console.debug(_filter)
        _generator = _filter(_generator)
    return _generator


def iter_zip_files(
    zip_files: typing.Iterable[pathlib.Path],
) -> typing.Iterable[pathlib.Path]:
    # iter files from a passed iterator
    # e.g. a glob("*.file_ext") generator
    # init zip file schema validation
    for zip_file in zip_files:
        # validate uploaded zip file via the schema
        # applied is_valid_file() and has_valid_content() func
        errors = upload_file_schema.validate({"zip_file": zip_file})
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
        for json_file in libdrm.datamodels.upload.iter_content(zip_file):
            yield json_file


def iter_json_file_content(
    json_files: typing.Iterable[zipfile.ZipExtFile],
) -> typing.Iterable[collections.OrderedDict]:
    # Receive ZipExtFile based JSON files and yield JSON decoded bytes.
    for json_file in json_files:
        for _bytes in json_file:
            # filter out rows with invalid JSON format
            # NOTE:
            # we can only validate JSON formatted data through the schema
            # Hence, we need to first validate the raw bytes data with an ad hoc try/except method.
            if not libdrm.datamodels.disaster.DisasterModel.valid_json_bytes(_bytes):
                console.warning("Invalid JSON format. Skipping {}".format(_bytes))
                continue
            # yield JSON dict safely loaded from bytes via the marshmallow schema validator
            # the following fields are updated at runtime via the marshmallow schema model:
            #   - disaster_type (from global env if missing from bytes data)
            #   - uploaded_at
            #   - text_sanitized
            #   - annotations
            #   - img
            yield libdrm.datamodels.disaster.DisasterModel.safe_load_bytes(_bytes)


def iter_in_batch(
    data_points: typing.Iterable[collections.OrderedDict],
    batch_size=int(os.getenv("BATCH_ANNOTATE_SIZE", 100))
) -> typing.Iterable[dict]:
    batch = []
    for data_point in data_points:
        batch.append(data_point)
        if len(batch) == batch_size:
            yield {"batch": batch}
            # flush batch
            batch = []
        #  Ensure to yield all data points.
        #  Also when the their total number is
        #  lesser that the batch_size.
        if len(batch) > 0:
            yield {"batch": batch}
        continue


def process_uploads(files: typing.Iterable[pathlib.Path], extra_steps: typing.Iterable[typing.Callable] = None):
    # zip file processing pipeline steps for each data point (i.e. disaster event)
    filters = [
        iter_zip_files,
        iter_zip_file_content,
        iter_json_file_content,
        iter_in_batch,
    ]
    if extra_steps is not None:
        filters.extend(extra_steps)
    return pipe_and_filter(files, filters)
