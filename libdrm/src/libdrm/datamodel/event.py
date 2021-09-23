# -*- coding: utf-8 -*-

import dataclasses
import datetime
import json
import typing

import pytz

from .config import Config


@dataclasses.dataclass()
class DisasterEvent:
    """
    DisasterEvent class creates instances of events user uploaded files.
    """

    # default event properties
    created_at: str
    lang: str
    text: str
    uploaded_at: str = datetime.datetime.now(pytz.timezone(Config.timezone)).isoformat()

    # runtime event properties
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized: str = None
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotation: dict = None
    # img dictionary contains image metadata e.g., path, size, format, etc.
    img: dict = None

    @classmethod
    def from_dict(cls, data: dict):
        class_fields = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in class_fields})

    @classmethod
    def from_bytes(cls, event: bytes):
        return cls.from_dict(json.loads(event))

    def to_dict(self):
        return vars(self)

    def to_bytes(self):
        return json.dumps(self.to_dict()).encode("utf-8")

    def sanitize_text(self, sanitizer: typing.Callable):
        self.text_sanitized = sanitizer(self.text)

    def annotate_text(self, annotator: typing.Callable, model_type: str):
        self.annotation[model_type] = annotator(self.text)
