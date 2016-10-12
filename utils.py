import config


def print_debug(message):
    """Print the debug message if debug mode is turned on."""
    if not config.debug_mode:
        return
    print('DEBUG: %s' % message)
