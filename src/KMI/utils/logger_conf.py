"""Module for basic logging config. Creating only one logger object. Default is logging to file and stdout."""

import datetime
import logging
import logging.config
from pathlib import Path

_logs_path = Path.cwd() / "logs"
_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
STANDARD_FORMAT = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
VERBOSE_FORMAT = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s] [%(levelname)s] %(message)s"

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': VERBOSE_FORMAT,
        },

        'standard': {
            'format': STANDARD_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': f'{_logs_path}/KMI_{_now}.log',
        },
    },
    'loggers': {
        'KMI': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            # 'propagate': False, # Do not propagate to root logger
        },
    },
}

_logs_path.mkdir(parents=True, exist_ok=True)
logging.config.dictConfig(LOGGING_CONFIG)
_global_logger: logging.Logger = logging.getLogger('KMI')
logger = _global_logger

def get_global_logger() -> logging.Logger:
    """Return the global logger object."""
    return _global_logger
