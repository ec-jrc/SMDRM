import os
import pytest
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.annotator import FiresAnnotator


@pytest.fixture()
def fires():
    yield FiresAnnotator()
