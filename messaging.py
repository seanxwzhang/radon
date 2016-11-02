# Messaging Subsystem
import requests
import config
import utils

slack_enabled = True
json_payload = '{"text": "%s"}'

slack_messages = {
    404: '*HTTP 404*\nURL: {0}{1}\nreferer: {2}\nUser-Agent: {3}',
    500: '*HTTP 500*\nURL: {0}{1}\nReferrre: {2}\nUser-Agent: {3}',
}
email_template = 'This email is sent from an automatic monitor program running on server.'


def send_slack_message(message):
    if not slack_enabled:
        return
    payload = json_payload % message
    r = requests.post(config.slack_url, data=payload)
    utils.print_debug('Slack message sent %s' % payload)
    if r.status_code != 200:
        utils.print_error('Failed to sent slack message: %s' % payload)


def toggle_slack_message(status):
    global slack_enabled
    print('DEBUG: slack is toggled to %s' % status)
    if status == '0':
        slack_enabled = False
    elif status == '1':
        slack_enabled = True


def add_to_email_queue(content):
    if config.debug_mode:
        print('DEBUG: Added to email queue: %s' % content)
    pass


def send_emails():
    pass
