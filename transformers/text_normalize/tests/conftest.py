import pytest


@pytest.fixture()
def text():
    return "RT \na text string,   &amp; to be normalized @API #NothingSpecial https://example.com http"


@pytest.fixture()
def batch_texts(text):
    return [text]
