"""Module for basic logging config. Creating only one logger object. Default is logging to file and stdout."""

import datetime
import logging
import logging.config
from pathlib import Path

_logs_path = Path.cwd() / "logs"
_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
STANDARD_FORMAT = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
VERBOSE_FORMAT = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s] [%(levelname)s] %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": VERBOSE_FORMAT,
        },
        "standard": {
            "format": STANDARD_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": f"{_logs_path}/KMI_{_now}.log",
        },
    },
    "loggers": {
        "KMI": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            # 'propagate': False, # Do not propagate to root logger
        },
    },
}

_logs_path.mkdir(parents=True, exist_ok=True)
logging.config.dictConfig(LOGGING_CONFIG)
_global_logger: logging.Logger = logging.getLogger(__package__)
logger = _global_logger


def get_global_logger() -> logging.Logger:
    """Return the global logger object."""
    return _global_logger


def get_child_file_logger(name: str) -> logging.Logger:
    """
    Creates and returns a child logger with a file handler.
    This function creates a child logger from a global logger, adds a file handler to it,
    and sets a formatter for the file handler. The log file will be named using the provided
    name and the current timestamp.

    Example:
        ```python
        from KMI.utils.logger_conf import get_child_file_logger
        child_logger = get_child_file_logger("exam")
        child_logger.info("This is a log message.") # This message will be logged to a file named "exam_<timestamp>.log"
        ```
    :param name: The name of the child logger.
    :return: A child logger with a file handler.
    """

    file_hdlr = logging.FileHandler(f"{_logs_path}/{name}_{_now}.log")
    file_formatter = logging.Formatter(VERBOSE_FORMAT)
    file_hdlr.setFormatter(file_formatter)
    child_logger: logging.Logger = _global_logger.getChild(name)
    child_logger.addHandler(file_hdlr)

    return child_logger
