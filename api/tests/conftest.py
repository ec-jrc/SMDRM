import os
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from wsgi import create_app

@pytest.fixture()
def app():
    config = {
        "TESTING": True,
        "MAX_CONTENT_LENGTH": 1000, # bytes
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config=config)

    # set up

    yield app

    # tear down

@pytest.fixture()
def client(app):
    return app.test_client()
