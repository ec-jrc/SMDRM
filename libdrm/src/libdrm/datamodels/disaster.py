from __future__ import annotations
import dataclasses
import datetime
import json
import marshmallow.validate
import os
import pytz
import typing


DISASTER_TYPES = [
    "floods",
    "fires",
]


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
    # we expect the disaster type to come from the user
    # either in the raw event or as a global env variable
    disaster_type: str
    # event upload datetime at initialization
    uploaded_at: str = datetime.datetime.now(
        pytz.timezone(os.getenv("TIMEZONE", "UTC"))
    ).isoformat()

    # runtime event properties to be populated by Sanitizer and Annotator APIs, respectively
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized: str = str()
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotations: dict = dataclasses.field(default_factory=dict)
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img: dict = dataclasses.field(default_factory=dict)

    @classmethod
    def is_valid_json(cls, data: bytes):
        # bytes is the input format from the zip file
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError:
            return False
        return True

    @classmethod
    def schema_serialize_from_bytes(cls, data: typing.Union[bytes, str]):
        schema = DisasterSchema()
        return cls.serialize_from_dict(schema.loads(data))

    @classmethod
    def schema_serialize_from_dict(cls, data: dict):
        schema = DisasterSchema()
        return cls.serialize_from_dict(schema.load(data))

    @classmethod
    def serialize_from_bytes(cls, data: bytes) -> DisasterModel:
        # convert passed data to JSON dict and load
        json_data = json.loads(data)
        return cls.serialize_from_dict(json_data)

    @classmethod
    def serialize_from_dict(cls, data: dict) -> DisasterModel:
        # build object from dict with required fields only
        class_fields = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in class_fields})

    def deserialize_to_bytes(self) -> bytes:
        # convert self to dict and serialize to JSON
        return json.dumps(vars(self)).encode("utf-8")

    def deserialize_to_dict(self) -> dict:
        return json.loads(self.deserialize_to_bytes())


class DisasterSchema(marshmallow.Schema):
    # default data fields
    id = marshmallow.fields.Integer(required=True)
    created_at = marshmallow.fields.String(required=True)
    lang = marshmallow.fields.String(required=True)
    text = marshmallow.fields.String(required=True)
    # created at model init
    uploaded_at = marshmallow.fields.String()
    # we expect the disaster type coming from the user
    disaster_type = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(DISASTER_TYPES),
        required=True,
    )
    # runtime event properties to be populated by internal APIs
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized = marshmallow.fields.String(default="")
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotations = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.Str(),
        default=dict(),
    )
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.Str(),
        default=dict(),
    )

    class Meta:
        ordered = True
        unknown = marshmallow.EXCLUDE
