# Utility functions

import config
import sys


def print_debug(message):
    """Print the debug message if debug mode is turned on."""
    if not config.debug_mode:
        return
    print('DEBUG: %s' % message)


def print_error(message):
    """Print error message"""
    print('Error: %s' % message, file=sys.stderr)
