import pytest
import pathlib

import sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from src import annotator

# test annotators
floods_ita = annotator.FloodsAnnotator(lang="it")
floods_ml = annotator.FloodsAnnotator(lang="ml")


def test_get_model_id():
    """
    Test if FloodModel is initialized properly.
    """
    assert ".relevance-cnn-init.it" in floods_ita._get_model_id()


def test_model_init_in_italian():
    """
    Test initialization of FloodModel in Italian.
    """
    assert floods_ita.lang == "it"
    # exclude timestamp from name for atemporal test
    assert ".relevance-cnn-init.it" in floods_ita._model_id
    # tokenizer is available for this language but not the embeddings
    assert (
        hasattr(floods_ita, "_model")
        and hasattr(floods_ita, "_tokenizer")
        and not hasattr(floods_ita, "_embeddings")
    )


def test_model_init_in_multilingual():
    """
    Test initialization of FloodModel in Multilingual.
    """
    assert floods_ml.lang == "ml"
    assert floods_ml._model_id == "lasermultilingual"
    # tokenizer is available for this language but not the embeddings
    assert (
        hasattr(floods_ml, "_model")
        and hasattr(floods_ml, "_embeddings")
        and not hasattr(floods_ml, "_tokenizer")
    )


def test_model_it_infer_on_junk():
    """
    Test inference (predictions) of Italian FloodModel on junk text.
    """
    sample_text = tuple(["Il calcio è andato a Roma."])
    result = floods_ita.infer(sample_text)[0]
    assert result == pytest.approx(0.007, 0.1)


def test_model_it_infer_on_flood():
    """
    Test inference (predictions) of Italian FloodModel on flood related text.
    """
    sample_text = tuple(
        ["Piogge torrenziali stanno causando alluvioni ed inondazioni."]
    )
    result = floods_ita.infer(sample_text)[0]
    assert result == pytest.approx(0.44, 0.1)


def test_model_ml_infer_on_junk():
    """
    Test inference (predictions) of Multilingual FloodModel on junk text.
    """
    # `Il calcio è andato a Roma in Italia.` in Dutch
    sample_text = tuple(["Voetbal is naar Rome gegaan."])
    result = floods_ml.infer(sample_text)[0]
    assert result == pytest.approx(0.011, 0.1)


def test_model_ml_infer_on_flood():
    """
    Test inference (predictions) of Multilingual FloodModel on junk text.
    """
    sample_text = tuple(
        ["Проливные дожди поднимают уровень реки По и вызывают наводнения."]
    )
    result = floods_ml.infer(sample_text)[0]
    assert result == pytest.approx(0.65, 0.1)
