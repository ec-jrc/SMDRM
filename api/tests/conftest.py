import os
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import apiv1


@pytest.fixture()
def app():
    app = apiv1.create_app()
    app.config.update({
        "TESTING": True,
        "MAX_CONTENT_LENGTH": 1000 # bytes
    })

    # set up

    yield app

    # tear down


@pytest.fixture()
def client(app):
    return app.test_client()

