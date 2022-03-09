"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the CONFIG_TYPE environment variable
"""

# logging configuration
# https://flask.palletsprojects.com/en/1.0.x/logging/#logging
# https://stackoverflow.com/questions/51318988/why-flask-logger-does-not-log-in-docker-when-using-uwsgi-in-front
from flask import Flask, render_template
import logging
from logging.config import dictConfig
import os


# define logging config before the app initizalization
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(filename)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": "default",
            }
        },
        "root": {"level": os.getenv("LOG_LEVEL", "INFO"), "handlers": ["wsgi"]},
    }
)


# using root logger to merge flask and gunicorn logs
console = logging.getLogger()


### Application Factory ###
def create_app():

    app = Flask(__name__)
    console.debug(app.config)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logrotate(app)

    # Register error handlers
    register_error_handlers(app)

    return app


### Helper Functions ###
def register_blueprints(app):
    from app.annotate import annotate_blueprint
    from app.info import info_blueprint

    app.register_blueprint(annotate_blueprint, url_prefix="/model")
    app.register_blueprint(info_blueprint)


def initialize_extensions(app):
    pass


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("400.html"), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template("405.html"), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500


def configure_logrotate(app):
    """Use current_app.logger to write to log file."""
    from logging.handlers import RotatingFileHandler

    # create logrotate directory
    logs_dir = os.path.join(app.instance_path, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    console.debug("logs directory: {}".format(logs_dir))
    # create a file handler object
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, "app.log"), maxBytes=16384, backupCount=20
    )
    file_handler.setLevel(logging.WARNING)
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s(%(lineno)d): %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    # add file handler object to the app.logger
    # can be used via current_app.logger
    app.logger.addHandler(file_handler)
