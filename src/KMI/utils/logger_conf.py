"""Module for basic logging config. Creating only one logger object. Default is logging to file and stdout."""

import datetime
import logging
import os


def create_logger() -> None:
    """Create logger Basic config."""
    logs_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    os.makedirs(logs_path, exist_ok=True)
    file_name: str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f_log.txt")
    log_file: str = os.path.join(logs_path, file_name)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(pathname)s:%(lineno)s - %(funcName)s] [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
