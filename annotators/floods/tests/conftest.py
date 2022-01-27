import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from app.annotate import annotator

import pytest


@pytest.fixture(scope="module")
def floods_ita():
    yield annotator.FloodsAnnotator(lang="it")


@pytest.fixture(scope="module")
def floods_ml():
    yield annotator.FloodsAnnotator(lang="ml")

