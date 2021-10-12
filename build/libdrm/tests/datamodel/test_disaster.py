import collections

import pytest
import marshmallow

from libdrm import datamodels


def test_init(valid_json):
    """
    Test class __init__ method. All fields must be specified to use the default method.
    """
    valid_json.update(
        {"uploaded_at": "now", "text_sanitized": "", "annotation": 0.0, "img": {}}
    )
    m = datamodels.disaster.DisasterModel(**valid_json)
    required = m.get_required_fields()
    for k in valid_json:
        assert k in required


def test_init_invalid(valid_json):
    """
    DisasterModel should not be initialized with __init__ method
    if not all required fields are set
    """
    with pytest.raises(TypeError):
        datamodels.disaster.DisasterModel(**valid_json)


def test_valid_json_bytes(valid_bytes):
    """
    Test helper method to validate JSON formatted bytes.
    """
    assert datamodels.disaster.DisasterModel.valid_json_bytes(valid_bytes)


def test_invalid_json_bytes():
    """
    Test helper method to validate JSON formatted bytes.
    """
    assert not datamodels.disaster.DisasterModel.valid_json_bytes(
        b"not a JSON formatted bytes data"
    )


def test_save_load_bytes(valid_bytes):
    m = datamodels.disaster.DisasterModel.safe_load_bytes(valid_bytes)
    assert isinstance(m, collections.OrderedDict)


def test_save_load_dict(valid_json):
    m = datamodels.disaster.DisasterModel.safe_load_dict(valid_json)
    assert isinstance(m, collections.OrderedDict)


def test_serialize_from_bytes_invalid(invalid_bytes):
    """
    Validation against schema fails because of missing keys and return marshmallow exception.
    """
    with pytest.raises(marshmallow.exceptions.ValidationError):
        datamodels.disaster.DisasterModel.from_bytes(invalid_bytes)


def test_serialize_from_dict_invalid(invalid_json):
    """
    Validation against schema fails because of missing keys and return marshmallow exception.
    """
    with pytest.raises(marshmallow.exceptions.ValidationError):
        datamodels.disaster.DisasterModel.from_dict(invalid_json)


def test_deserialize_to_string(valid_json):
    m = datamodels.disaster.DisasterModel.from_dict(valid_json)
    assert isinstance(m, datamodels.disaster.DisasterModel)
    deserialized = m.to_string()
    assert isinstance(deserialized, str)


def test_deserialize_to_dict(valid_json):
    m = datamodels.disaster.DisasterModel.from_dict(valid_json)
    assert isinstance(m, datamodels.disaster.DisasterModel)
    deserialized = m.to_dict()
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
