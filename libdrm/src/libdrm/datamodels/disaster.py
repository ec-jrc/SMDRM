from __future__ import annotations
import dataclasses
import datetime
import json
import os
import typing
import pytz

from libdrm.nicelogging import console_logger


console = console_logger("libdrm.datamodels.event")


@dataclasses.dataclass()
class DisasterModel:
    """
    DisasterEventModel class creates instances of disaster events from user-uploaded files.
    """

    # default data fields
    id: str
    created_at: str
    lang: str
    text: str
    disaster_type: str  # we expect the disaster type coming from the user
    uploaded_at: str = datetime.datetime.now(
        pytz.timezone(os.getenv("TIMEZONE", "UTC"))
    ).isoformat()

    # runtime event properties to be populated by Sanitizer and Annotator APIs, respectively
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized: str = None
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotations: dict = dataclasses.field(default_factory=dict)
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def validate_json(cls, data: bytes):
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError as err:
            console.exception(err)
            console.debug(data)
            return False
        return True

    @classmethod
    def from_dict(cls, data: dict) -> DisasterModel:
        # build object from dict with required fields only
        class_fields = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in class_fields})

    @classmethod
    def from_bytes(cls, data: bytes) -> DisasterModel:
        # convert passed data to JSON dict and load
        json_data = json.loads(data)
        return cls.from_dict(json_data)

    def to_bytes(self) -> bytes:
        # convert self to dict and serialize to JSON
        return json.dumps(vars(self)).encode("utf-8")

    def to_dict(self) -> dict:
        return json.loads(self.to_bytes())

    def sanitize_text(self, sanitizer: typing.Callable) -> None:
        self.text_sanitized = sanitizer(self.text)

    def annotate_text(self, annotator: typing.Callable) -> None:
        self.annotations[self.disaster_type] = annotator(self.text_sanitized)

    def add_disaster_type(self, disaster_type: str) -> None:
        self.disaster_type = disaster_type

    @property
    def is_ready(self):
        # event is annotated
        # TODO: and geotagged
        return bool(self.annotations)
