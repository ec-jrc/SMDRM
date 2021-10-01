# -*- coding: utf-8 -*-

"""
Custom Logging Class to handle console and file outputs.

Logging level ranking

|Value | Level    |
|------|----------|
|50    | CRITICAL |
|40    | ERROR    |
|30    | WARNING  |
|20    | INFO     |
|10    | DEBUG    |
|0     | NOTSET   |

"""

import json
import logging.config
import logging.handlers
import os
import time

# logging config
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s"
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", logging.INFO)
LOG_FILE_SIZE_MB = int(os.getenv("LOG_FILE_SIZE_MB", 32))
LOG_FILE_BACKUPS = int(os.getenv("LOG_FILE_BACKUPS", 10))


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(vars(record))


def console_logger(name, level: str = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(level or LOGGING_LEVEL)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(handler)
    return logger


def file_logger(name, path, level: str = None):
    # https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        backupCount=LOG_FILE_BACKUPS,
        filename="{path}/{fn}.log".format(path=path, fn=name),
        maxBytes=1048576 * LOG_FILE_SIZE_MB,
        mode="a",
    )
    handler.setLevel(level or LOGGING_LEVEL)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger
