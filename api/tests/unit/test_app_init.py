def test_config(app):
    """Test app initialization with default and manual config."""
    assert app.config['TESTING']
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    assert app.config["MAX_CONTENT_LENGTH"] == 1000

def test_registered_blueprint(app):
    """Test if main blueprint is registered to the app."""
    bp = app.blueprints['api']
    assert bp.name == "api"
    assert bp.url_prefix == "/api/v1"


def test_api_blueprint_root(client):
    """Given the root of the main blueprint is api/v1/
    test if api/v1 endpoint returns successful code.
    """
    res = client.get('/api/v1/')
    assert res.status_code == 200
    assert b"<title>SMDRM API</title>" in res.data
