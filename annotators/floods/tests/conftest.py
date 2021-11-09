import os
import pytest
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.annotator import FloodsAnnotator


@pytest.fixture()
def floods_ita():
    yield FloodsAnnotator(lang="it")


@pytest.fixture()
def floods_ml():
    yield FloodsAnnotator(lang="ml")
