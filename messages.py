# Messaging Subsystem
import requests
import config

slack_enabled = False
json_payload = '{"text": "%s"}'

slack_messages = {
    404: '*HTTP 404*\nURL: {0}{1}\nreferer: {2}\nUser-Agent: {3}',
    500: '*HTTP 500*\nURL: {0}{1}\nReferrre: {2}\nUser-Agent: {3}'
}
email_template = 'This email is sent from an automatic monitor program running on server.'


def send_slack_message(message_type, url, referer, agent):
    if not slack_enabled:
        return
    message = slack_messages[message_type].format(config.domain_name, url, referer, agent)
    payload = json_payload % message
    r = requests.post(config.slack_url, data=payload)
    if config.debug_mode:
        print('DEBUG: Slack message sent %s' % payload)
    if r.status_code != 200:
        print('ERROR: Failed to post message to slack. Status code {0}. Payload: {1}'.format(r.status_code, payload))


def toggle_slack_message(status):
    global slack_enabled
    print('DEBUG: slack is toggled to %s' % status)
    if status == '0':
        slack_enabled = False
    elif status == '1':
        slack_enabled = True
    else:
        pass    # Do nothing if that's something other than 0 or 1


def add_to_email_queue(content):
    if config.debug_mode:
        print('DEBUG: Added to email queue: %s' % content)
    pass


def send_emails():
    pass
