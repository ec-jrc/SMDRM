import logging
import os


class Config:
    observing_interval: int = 60
    path_glob_pattern: str = "*.zip"


class DevConfig(Config):
    observing_interval: int = 5


class TestConfig(Config):
    observing_interval: int = 1


def get_config():
    env = os.getenv("ENV", "dev")
    config_lookup = {"prod": Config, "dev": DevConfig, "test": TestConfig}
    return config_lookup[env]


def nicelogging(name, level=logging.INFO):
    """
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

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
        )
    )
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOGGING_LEVEL", level))
    return logger
