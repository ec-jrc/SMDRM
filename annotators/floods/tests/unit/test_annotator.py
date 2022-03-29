# -*- coding: utf-8 -*-

import pytest


def test_model_init(model):
    """
    Test initialization of FloodModel in Multilingual.
    """
    assert hasattr(model, "_model")


def test_model_on_it(model):
    """Test inference of FloodModel on flood related text in italian."""
    sample_text = tuple(
        ["Piogge torrenziali stanno causando alluvioni ed inondazioni."]
    )
    result = model.infer(sample_text)[0]
    assert result == pytest.approx(0.44, 0.1)


def test_model_on_ru(model):
    """
    Test inference of FloodModel on flood related text in russian.
    """
    sample_text = tuple(
        ["Проливные дожди поднимают уровень реки По и вызывают наводнения."]
    )
    result = model.infer(sample_text)[0]
    assert result == pytest.approx(0.65, 0.1)

