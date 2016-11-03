# Utility functions

import config
import sys

from datetime import datetime


def print_debug(message):
    """Print the debug message if debug mode is turned on."""
    if not config.debug_mode:
        return
    print("[{0}] Debug: {1}".format(datetime.now(), message))


def print_error(message):
    """Print error message to stderr and write to log file at the same time"""
    print("[{0}] Error: {1}".format(datetime.now(), message), file=sys.stderr)
    log_file.write("[{0}] Error: {1}\n".format(datetime.now(), message))


log_file = open(config.log_file_path, 'a')
