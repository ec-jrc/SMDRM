import os
import logging
from logging.handlers import RotatingFileHandler

## FLASK APP HELPERS

def _setup_logrotate(app, level=logging.WARNING):
    """Configure an app instance logrotate file to log warnings, and
    higher log events. Use current_app.logger to log events to file."""

    # ensure the logs directory exists
    path = os.path.join(app.instance_path, "logs")
    os.makedirs(path, exist_ok=True)

    # create a file handler object
    file_handler = RotatingFileHandler(
        os.path.join(path, "app.log"),
        maxBytes=16384,
        backupCount=20,
    )
    file_handler.setLevel(level)
    # add file handler object to the app.logger
    # can be used via current_app.logger
    app.logger.addHandler(file_handler)
