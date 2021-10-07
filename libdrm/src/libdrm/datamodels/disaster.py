from __future__ import annotations
import dataclasses
import datetime
import json
import marshmallow.validate
import os
import pytz
import typing


ALLOWED_DISASTER_TYPES = [
    "floods",
    "fires",
]
# must fail if not passed
DISASTER_TYPE = os.environ["DISASTER_TYPE"]
TIMEZONE = pytz.timezone(os.getenv("TIMEZONE", "UTC"))


@dataclasses.dataclass()
class DisasterModel:
    """
    DisasterEventModel class creates instances of disaster events from user-uploaded files.
    """

    # default data fields
    id: int
    created_at: str
    lang: str
    text: str
    # we expect the disaster type to come from the user either in each
    # data point being uploaded or as a global environment variable
    disaster_type: str

    # uploaded_at, text_sanitized, annotations, and img data point properties are
    # populated at runtime via the marshmallow schema model
    uploaded_at: str
    text_sanitized: str
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotation: float
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img: dict

    @classmethod
    def valid_json_bytes(cls, data: bytes):
        # bytes is the input format from the zip file
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError:
            return False
        return True

    @classmethod
    def get_required_fields(cls) -> set:
        return {f.name for f in dataclasses.fields(cls)}

    @classmethod
    def safe_load_bytes(cls, data: typing.Union[bytes, str]) -> dict:
        return DisasterSchema().loads(data)

    @classmethod
    def safe_load_dict(cls, data: dict) -> dict:
        return DisasterSchema().load(data)

    @classmethod
    def from_bytes(cls, data: typing.Union[bytes, str]) -> DisasterModel:
        # serialize JSON bytes to object
        return cls(**DisasterSchema().loads(data))

    @classmethod
    def from_dict(cls, data: dict) -> DisasterModel:
        # serialize JSON dict to object
        return cls(**DisasterSchema().load(data))

    def to_string(self) -> str:
        # deserialize self to JSON string
        return DisasterSchema().dumps(self)

    def to_dict(self) -> dict:
        # deserialize self to JSON dict
        return DisasterSchema().dump(self)


class DisasterSchema(marshmallow.Schema):
    # default data fields
    id = marshmallow.fields.Integer(required=True)
    created_at = marshmallow.fields.String(required=True)
    lang = marshmallow.fields.String(required=True)
    text = marshmallow.fields.String(required=True)
    # we expect the disaster type coming from the user,
    # user can choose to mark disaster type by data point of globally.
    disaster_type = marshmallow.fields.String(
        # validate if present
        validate=marshmallow.validate.OneOf(ALLOWED_DISASTER_TYPES),
        # else add from global env
        missing=DISASTER_TYPE,
    )
    # data point properties to be populated at runtime
    # created at model init
    uploaded_at = marshmallow.fields.String(
        missing=datetime.datetime.now(TIMEZONE).isoformat(),
    )
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized = marshmallow.fields.String(missing="")
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotation = marshmallow.fields.Float(
        missing=0.0,
    )
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.Str(),
        missing=dict(),
    )

    class Meta:
        ordered = True
        unknown = marshmallow.EXCLUDE
