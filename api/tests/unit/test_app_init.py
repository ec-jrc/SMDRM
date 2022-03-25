from conftest import apiv1 

def test_config():
    """Test app initialization with default and manual config."""
    assert not apiv1.create_app().testing
    assert apiv1.create_app({'TESTING': True}).testing


def test_registered_blueprint(app):
    """Test if main blueprint is registered to the app."""
    bp = app.blueprints['api']
    assert bp.name == "api"


def test_blueprint_url_prefix():
    """Test the main blueprint url prefix."""
    assert apiv1.blueprint.url_prefix == "/api/v1"


def test_api_blueprint_root(client):
    """Given the root of the main blueprint is api/v1/
    test if api/v1 endpoint returns successful code.
    """
    res = client.get('/api/v1/')
    assert res.status_code == 200
    assert b"<title>SMDRM API</title>" in res.data
