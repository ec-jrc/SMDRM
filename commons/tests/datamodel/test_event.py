# -*- coding: utf-8 -*-

import pytest

from libdrm.datamodel import DisasterEvent


# test data
valid_test_data = dict(
    created_at="Sat May 15 08:49:13 +0000 2021",
    text="A text to be annotated with floods model",
    lang="it",
)

invalid_test_data = dict(
    unknown_type=True,
)


# valid fields
valid_fields = ["created_at", "lang", "text"]


def test_successful_class_init():
    """
    Test class __init__ method.
    """
    event = DisasterEvent(**valid_test_data)
    assert event.created_at == "Sat May 15 08:49:13 +0000 2021"
    assert event.lang == "it"
    assert event.text == "A text to be annotated with floods model"


def test_successful_class_from_dict():
    """
    Test class from_dict method.
    """
    event = DisasterEvent.from_dict(valid_test_data)
    assert event.created_at == "Sat May 15 08:49:13 +0000 2021"
    assert event.lang == "it"
    assert event.text == "A text to be annotated with floods model"


def test_fail_class_init():
    """
    Expects the following exception:
        TypeError: __init__() got an unexpected keyword argument 'unknown_type'
    """
    with pytest.raises(TypeError):
        DisasterEvent(**invalid_test_data)
