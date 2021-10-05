import pytest
import marshmallow

from libdrm import datamodels


def test_init(valid_json):
    """
    Test class __init__ method.
    """
    m = datamodels.disaster.DisasterModel(**valid_json)
    assert m.id == 123456789
    assert m.created_at == "Sat May 15 08:49:13 +0000 2021"
    assert m.lang == "it"
    assert m.text == "A text to be annotated with floods model"
    assert m.disaster_type == "floods"


def test_is_valid_json(valid_bytes):
    """
    Test is_valid_json() helper method to validate JSON formatted bytes.
    """
    assert datamodels.disaster.DisasterModel.is_valid_json(valid_bytes)


def test_schema_serialize_from_bytes(valid_bytes):
    m = datamodels.disaster.DisasterModel.schema_serialize_from_bytes(valid_bytes)
    for f in (
        "uploaded_at",
        "text_sanitized",
        "annotations",
        "img",
    ):
        assert hasattr(m, f), "{} field is missing".format(f)


def test_schema_serialize_from_dict(valid_json):
    m = datamodels.disaster.DisasterModel.schema_serialize_from_dict(valid_json)
    for f in (
        "uploaded_at",
        "text_sanitized",
        "annotations",
        "img",
    ):
        assert hasattr(m, f), "{} field is missing".format(f)


def test_schema_serialize_from_bytes_invalid(invalid_bytes):
    """
    Validation against schema fails because of missing keys and return marshmallow exception.
    """
    with pytest.raises(marshmallow.exceptions.ValidationError):
        datamodels.disaster.DisasterModel.schema_serialize_from_bytes(invalid_bytes)


def test_schema_serialize_from_dict_invalid(invalid_bytes):
    """
    Validation against schema fails because of missing keys and return marshmallow exception.
    """
    with pytest.raises(marshmallow.exceptions.ValidationError):
        datamodels.disaster.DisasterModel.schema_serialize_from_dict(invalid_bytes)


def test_serialize_from_bytes_invalid(invalid_bytes):
    """
    Raises TypeError because of data is not validated against schema.
    """
    with pytest.raises(TypeError):
        datamodels.disaster.DisasterModel.serialize_from_bytes(invalid_bytes)


def test_serialize_from_dict_invalid(invalid_json):
    """
    Raises TypeError because of data is not validated against schema.
    """
    with pytest.raises(TypeError):
        datamodels.disaster.DisasterModel.serialize_from_dict(invalid_json)


def test_deserialize_to_bytes(valid_json):
    m = datamodels.disaster.DisasterModel.schema_serialize_from_dict(valid_json)
    assert isinstance(m, datamodels.disaster.DisasterModel)
    deserialized = m.deserialize_to_bytes()
    assert isinstance(deserialized, bytes)


def test_deserialize_to_dict(valid_json):
    m = datamodels.disaster.DisasterModel.schema_serialize_from_dict(valid_json)
    assert isinstance(m, datamodels.disaster.DisasterModel)
    deserialized = m.deserialize_to_dict()
    assert isinstance(deserialized, dict)


def test_disaster_schema_with_valid_data(valid_json):
    schema = datamodels.disaster.DisasterSchema()
    errors = schema.validate(valid_json)
    assert not errors


def test_disaster_schema_with_invalid_data(invalid_json):
    schema = datamodels.disaster.DisasterSchema()
    errors = schema.validate(invalid_json)
    assert errors == {
        "created_at": ["Missing data for required field."],
        "lang": ["Missing data for required field."],
        "text": ["Missing data for required field."],
        "disaster_type": ["Must be one of: floods, fires."],
    }
