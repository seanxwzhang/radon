# URL Filter for Log Monitor
import urllib.parse

import radon.config as config
import radon.dbo as dbo
import radon.messages as messages

cacheable_params = None
host_ignore_list = None
url_ignore_pattern = None
agent_ignore_pattern = None


def load_cacheable_param():
    global cacheable_params
    cacheable_params = dbo.load_string_list('cacheable_param', 'param')


def load_host_ignore():
    global host_ignore_list
    host_ignore_list = dbo.load_string_list('host_ignore_list', 'host')


def load_url_ignore():
    global url_ignore_pattern
    url_ignore_pattern = dbo.load_pattern_list('url_ignore_list', 'pattern')


def load_agent_ignore():
    global agent_ignore_pattern
    agent_ignore_pattern = dbo.load_pattern_list('agent_ignore_list', 'keyword')


def filter_cacheable_param(url):
    global cacheable_params
    if '?' not in url:
        return url
    index = url.find('?')
    filtered_param = []
    params = url[index + 1:].split('&')
    for param in params:
        key = param.split('=')[0]
        if key in cacheable_params:
            filtered_param.append(param)

    filtered_url = url[:index]
    if len(filtered_param) > 0:
        filtered_url += '?' + '&'.join(filtered_param)
    return filtered_url


def filter_request(entry):
    """Return True if the result should be displayed on screen"""
    host = entry['host']
    if host in host_ignore_list:
        if config.debug_mode:
            print('DEBUG: ignore host %s' % host)
        return False

    request = entry['request']
    status = entry['status']
    arr = request.split()
    if len(arr) < 3:
        if config.debug_mode:
            print('DEBUG: len < 3: %s' % request)
        return False

    method = arr[0]
    url = urllib.parse.unquote(arr[1])
    if method != 'GET' or status == '304' or agent_ignore_pattern.search(entry['agent']):
        return False
    if status in ['401', '403', '404', '500', '503']:
        if agent_ignore_pattern.search(url):
            return False
        else:
            messages.send_slack_message(404, url, entry['referer'], entry['agent'])
            messages.add_to_email_queue(' '.join(entry))
            dbo.store_error_request(entry)
            return True
    if status == '200':
        if url_ignore_pattern.search(url):
            return False
        else:
            dbo.store_visited_url(filter_cacheable_param(url))
            return True  # Report 200 too
    return True
load_cacheable_param()
load_host_ignore()
load_url_ignore()
load_agent_ignore()

