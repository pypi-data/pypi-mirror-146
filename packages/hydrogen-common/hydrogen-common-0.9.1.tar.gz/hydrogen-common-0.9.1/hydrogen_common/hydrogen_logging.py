"""
hydrogen_logging

# Defines function to set up the python logger using hydrogen conventions.
"""

import logging
import os
import time

from .directory_paths import get_data_directory


def hydrogen_setup_logger():
    """Configure the python logging to write log messages to a standard place."""

    dirpath = get_data_directory()
    log_file = None
    if dirpath is not None:
        log_dir = f"{dirpath}/logs"
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
            os.chmod(log_dir, 0o777)
        today = time.strftime('%Y-%m-%d')
        log_file = f"{log_dir}/hydrogen-{today}.log"
        if not os.path.exists(log_file):
            with open(log_file, "w+") as stream:
                stream.write("")
            os.chmod(log_file, 0o777)

    logging.Formatter.converter = time.gmtime
    if log_file is not None:
        # Configure the python logger to log into this file
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s %(levelname)s:%(message)s',
            level=logging.INFO,
        )
