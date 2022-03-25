import os
from flask import Flask
from flask import Blueprint
from flask_restx import Api

# API namespaces
from apis.info import ns as info_ns
from apis.upload import ns as upload_ns

# API main blueprint setting root and version
blueprint = Blueprint("api", __name__, url_prefix='/api/v1')

# API instance
api = Api(
    blueprint,
    title='SMDRM API',
    version='1.0',
    description='Allows the end-user to interacts with the SMDRM components.',
    # All API metadatas
)

# add flask app factory method
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # app dev config
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        # allow uploads of max 64 mb
        MAX_CONTENT_LENGTH=64 * 10**6,
        # dev database
        DATABASE=os.path.join(app.instance_path, 'dev.sqlite'),
    )     

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # log config for debugging purpose
    app.logger.debug(app.config)

    # register the API blueprint
    app.register_blueprint(blueprint)

    # logrotate (level=WARNING)
    configure_logrotate(app)

    return app

# add namespaces to API
api.add_namespace(info_ns)
api.add_namespace(upload_ns)


## FLASK APP HELPERS

def configure_logrotate(app):
    """Configure an app instance logrotate file to log warnings, and
    higher log events. Use current_app.logger to log events to file."""
    from logging.handlers import RotatingFileHandler

    # ensure the logs directory exists
    logsdir = os.path.join(app.instance_path, "logs")
    os.makedirs(logsdir, exist_ok=True)

    # create a file handler object
    file_handler = RotatingFileHandler(
        os.path.join(logsdir, "app.log"),
        maxBytes=16384,
        backupCount=20,
    )
    file_handler.setLevel('WARNING')
    # add file handler object to the app.logger
    # can be used via current_app.logger
    app.logger.addHandler(file_handler)

