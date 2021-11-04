"""
SMDRM Data Processing Pipeline enables the creation of ad hoc data processing pipeline
with regards to the task at hand using a combination of Template and Bridge Design Patterns.

Step Abstract Base Class set the `logic` that each Concrete Step Class must implement.

Pipeline Class establishes the Template to `build` a pipeline.
It also establishes a Bridge with the Step Class (See `steps: typing.Iterable[Step]` in init() method).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import json
import logging
import os
import pydantic
import pytz
import requests
import typing
import zipfile


# logging
console = logging.getLogger("libdrm.pipeline")
# timezone for upload datetime
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE", "UTC"))


class DisasterModel(pydantic.BaseModel, extra=pydantic.Extra.ignore):
    """Represents the Disaster Data Point Model.
    NOTES:
        `extra` argument instructs the Pydantic Base Model to ignore undefined fields."""

    # default fields
    id: int
    created_at: str
    lang: str
    text: str
    # opts
    # annotations
    annotations: typing.Optional[list] = []
    # location based fields
    latitude: typing.Optional[float]
    longitude: typing.Optional[float]
    place_name: typing.Optional[str]
    place_type: typing.Optional[str]
    # auto generated fields
    uploaded_at: str = datetime.datetime.now(TIMEZONE).isoformat()


class Step(ABC):
    """Represents an abstract Step of a Pipeline."""

    @abstractmethod
    def logic(self, iterable: typing.Iterable) -> typing.Iterable:
        pass


@dataclass
class ZipFilesToJSONFiles(Step):
    """Represents a Pipeline Step to iterate JSON files from uploaded zip files."""

    def logic(self, paths: typing.Iterable[str]) -> typing.Iterable[zipfile.ZipExtFile]:
        for path in paths:
            console.debug("Processing {}".format(path))
            with zipfile.ZipFile(path, "r") as zf:
                for json_file in zf.infolist():
                    with zf.open(json_file) as ext_file:
                        yield ext_file


@dataclass
class JSONFilesToJSONLines(Step):
    """Represents a Pipeline Step to iterate valid JSON bytes from JSON files."""

    def logic(self, files: typing.Iterable[zipfile.ZipExtFile]) -> typing.Iterable[dict]:
        for file in files:
            for bline in file:
                try:
                    # validate the raw bytes data with an ad hoc try/except method
                    raw_json = json.loads(bline)
                except json.decoder.JSONDecodeError:
                    # filter out rows with invalid JSON format
                    console.warning("Invalid JSON format. Skipping {}".format(bline))
                    continue
                yield raw_json


@dataclass
class LegacyJSONLinesParser(Step):
    """Represents a Pipeline Step to parse legacy raw JSON dictionary from JSON bytes."""

    # this field must contain the rew event for legacy data
    legacy_data_model_field = "tweet"

    def logic(self, json_lines: typing.Iterable[dict]) -> typing.Iterable[dict]:
        for json_line in json_lines:
            if self.legacy_data_model_field in json_line:
                # extract raw json in case of legacy data
                json_line = json_line[self.legacy_data_model_field]
            yield json_line


@dataclass
class JSONLinesToDataPoints(Step):
    """Represents a Pipeline Step to iterate valid JSON dictionaries from JSON bytes."""

    # deserialize DisasterModel object may be useful for API calls
    deserialize: bool = False

    def logic(self, json_lines: typing.Iterable[dict]) -> typing.Iterable[typing.Union[dict, DisasterModel]]:
        for json_line in json_lines:
            try:
                data_point = DisasterModel(**json_line)
            except pydantic.error_wrappers.ValidationError:
                # filter out rows with invalid JSON format
                console.warning("Pydantic validation failed. Skipping {}".format(json_line))
                continue
            yield data_point.dict() if self.deserialize else data_point


@dataclass
class InBatches(Step):
    """Represents a Pipeline Step to iterate JSON bytes in batches."""

    # the number of data points to process at once
    batch_size: int = 10

    def logic(self, lines: typing.Iterable[typing.Union[bytes, dict, DisasterModel]]) -> typing.Iterable[list]:
        batch = []
        # line can be either bytes, dictionary, or DisasterModel
        for line in lines:
            batch.append(line)
            if len(batch) == self.batch_size:
                yield batch
                # flush batch
                batch = []
            continue
        #  Ensure to yield all data points.
        #  Also when the their total number is
        #  lesser that the batch_size.
        if len(batch) > 0:
            yield batch


@dataclass
class AnnotateInBatches(Step):
    """Represents a Pipeline Step to annotate batches of data points."""

    # the annotation API url endpoint
    endpoint: str

    def logic(self, batches: typing.Iterable[list]) -> typing.Iterable[list]:
        for batch in batches:
            response = requests.post(self.endpoint, json={"batch": batch})
            console.debug("AnnotateInBatches status code: [{}]".format(response.status_code))
            annotated = response.json()
            yield annotated["batch"]


@dataclass
class BatchesToElasticSearch(Step):
    """Represents a Pipeline Step to cache annotate batches of data points to ElasticSearch."""

    # ElasticSearch Client
    ElasticSearchClient = typing.TypeVar("ElasticSearchClient")
    client: ElasticSearchClient

    def logic(self, batches: typing.Iterable[dict]) -> typing.Union[typing.Iterable[dict], requests.Response]:
        for batch in batches:
            response = self.client.bulk_insert(data_points=batch)
            console.debug("BatchesToElasticSearch status code: [{}]".format(response.status_code))
            yield batch, response.json()


@dataclass
class Pipeline:
    """Represents a Pipeline of Steps for processing data."""

    input_iterable: typing.Iterable
    steps: typing.Iterable[Step]

    def build(self) -> typing.Iterable:
        """Build the pipeline given the steps."""
        iterable = self.input_iterable
        for step in self.steps:
            iterable = step.logic(iterable)
        return iterable
