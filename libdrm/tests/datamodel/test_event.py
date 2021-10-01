# -*- coding: utf-8 -*-

import pytest
import json

from libdrm.datamodels import DisasterEventModel


# test data
valid_test_data = dict(
    id="0123456789",
    created_at="Sat May 15 08:49:13 +0000 2021",
    text="A text to be annotated with floods model",
    lang="it",
)

invalid_test_data = dict(
    unknown_type=True,
)


# valid fields
valid_fields = ["created_at", "lang", "text"]


def test_init():
    """
    Test class __init__ method.
    """
    m = DisasterEventModel(**valid_test_data)
    assert m.id == "0123456789"
    assert m.created_at == "Sat May 15 08:49:13 +0000 2021"
    assert m.lang == "it"
    assert m.text == "A text to be annotated with floods model"


def test_from_dict():
    """
    Test class from_dict method.
    """
    m = DisasterEventModel.from_dict(valid_test_data)
    assert isinstance(m, DisasterEventModel)


def test_from_bytes():
    """
    Test class from_dict method.
    """
    bytes_data = json.dumps(valid_test_data).encode("utf-8")
    assert isinstance(bytes_data, bytes)
    m = DisasterEventModel.from_bytes(bytes_data)
    assert isinstance(m, DisasterEventModel)


def test_to_dict():
    m = DisasterEventModel(**valid_test_data)
    assert isinstance(m.to_dict(), dict)


def test_to_bytes():
    m = DisasterEventModel(**valid_test_data)
    assert isinstance(m.to_bytes(), bytes)


def test_sanitize_text():
    """
    Test if DisasterEventModel.sanitize_text() assigns the sanitized
    text from the passed callable to text_sanitized property.
    """

    def mocked_sanitizer(fake_arg):
        return "a mock to test the DisasterEventModel.sanitize_text() method"

    m = DisasterEventModel(**valid_test_data)
    m.sanitize_text(mocked_sanitizer)
    assert m.text_sanitized == "a mock to test the DisasterEventModel.sanitize_text() method"


def test_annotate_text():
    """
    Test if DisasterEventModel.annotate_text() assigns the annotation
    score and disaster type from the passed ML Model to annotations (dict) property.
    """

    def mocked_annotator(fake_arg):
        return annotation_score

    m = DisasterEventModel(**valid_test_data)
    model_type = "mocked"
    annotation_score = 0.9999
    m.annotate_text(mocked_annotator, model_type=model_type)
    assert m.annotations == {model_type: annotation_score}


def test_fail_class_init():
    """
    Expects the following exception:
        TypeError: __init__() got an unexpected keyword argument 'unknown_type'
    """
    with pytest.raises(TypeError):
        DisasterEventModel(**invalid_test_data)
