import os
import sys
# this allow to import normalize.py module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import annotator

fires = annotator.FiresAnnotator()


def test_model_init():
    assert "RobertaForSequenceClassification" in str(fires._model)
