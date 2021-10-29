import pytest
import pathlib

import sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from src import annotator


# test annotators
fires = annotator.FiresAnnotator()


def test_model_init():
    assert "RobertaForSequenceClassification" in str(fires._model)
