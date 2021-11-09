import pytest


def test_model_init(fires):
    assert "RobertaForSequenceClassification" in str(fires._model)
