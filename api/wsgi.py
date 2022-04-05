import os
from flask import Flask

from apiv1 import blueprint
from api.core.logging import _setup_logrotate


# add flask app factory method
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # app dev config
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        # allow uploads of max 64 mb
        MAX_CONTENT_LENGTH=64 * 10**6,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # swagger
        RESTX_MASK_SWAGGER=False,
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
    _setup_logrotate(app)

    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="""SMDRM API manager."""
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host IP address. Default is %(default)s."
    )
    parser.add_argument(
        "--port", default=5000, help="Host port. Default is %(default)s."
    )
    parser.add_argument(
        "--debug", action="store_true", default=False,
        help="Enables runtime debug mode to reload app at every file change. Default is %(default)s."
    )
    args = parser.parse_args()
    app = create_app()

    app.run(debug=args.debug, host=args.host, port=args.port)
