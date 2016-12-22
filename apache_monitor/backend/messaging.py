# Radon Project
# Created by Xinyu Chen

# messaging.py
# Messaging Subsystem
# This module handles all messaging and notification service

import config
import requests
import utils

slack_enabled = False
json_payload = '{"text": "{0}"}'


def send_slack_message(message):
    if not slack_enabled:
        return
    payload = json_payload.format(message)
    response = requests.post(config.slack_url, data=payload)
    utils.print_debug('Slack message sent {0}'.format(payload))
    if response.status_code != 200:
        utils.print_error('Failed to sent slack message: {0}'.format(payload))


def toggle_slack_message(status):
    global slack_enabled
    utils.print_debug('slack is toggled to %s' % status)
    if status == '0':
        slack_enabled = False
    elif status == '1':
        slack_enabled = True


def add_to_email_queue(content):
    if config.debug_mode:
        utils.print_debug('DEBUG: Added to email queue: %s' % content)
    pass


def send_emails():
    pass
