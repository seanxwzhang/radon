# Apache Log Monitor
# Created by Xinyu Chen, based on previous monitor module written by Tianyang Wen

import collections
import re
import subprocess
import sys

from colorama import Fore

import radon.config as config
import radon.messages as messages
import radon.dbo as dbo
import radon.logfilter as logfilter
import radon.logparser as logparser


def toggle_debug(status):
    if status == '0':
        config.toggle_debug(False)
    elif status == '1':
        config.toggle_debug(True)
        print('DEBUG: debug_mode is set to True')
    else:
        pass    # Do nothing if that's something other than 0 or 1


def do_nothing(param):
    pass


operations = {
    'slack': messages.toggle_slack_message,
    'debug': toggle_debug
}
operations = collections.defaultdict(lambda: do_nothing, operations)


# Check the query string for special commands
# @param    {str}   The incoming URL
# @return   {bool}  True if the url is a special command
def check_commands(request):
    # TODO Maybe we need to add security check before proceed to execute the commands
    # TODO Add a table to record operations happens here, including date & time
    arr = request.split()
    if len(arr) < 3:
        return False
    url = arr[1]
    if not url.startswith('goose.php?', 1):
        return False
    commands = url[11:].split('&')
    for command in commands:
        if config.debug_mode:
            print('DEBUG: %s' % command)
        parts = command.split('=')
        operations[parts[0]](parts[1])
    return True


# Main starts here
url_ignore_pattern = dbo.load_pattern_list('url_ignore_list', 'pattern')
agent_ignore_pattern = dbo.load_pattern_list('agent_ignore_list', 'keyword')
cacheable_param_pattern = dbo.load_pattern_list('cacheable_param', 'param')
host_ignore_list = dbo.load_string_list('host_ignore_list', 'host')

while True:
    line = sys.stdin.readline()
    if not line:
        break
    entry = logparser.parse(line)
    # check if the request has special control commands
    if check_commands(entry['request']):
        continue

    if logfilter.filter_request(entry):
        if entry['status'] == '200':
            color = Fore.GREEN
        else:
            color = Fore.RED
        print(color + entry['status'], end=' ')
        print(Fore.WHITE + entry['host'], end=' ')
        print(color + entry['request'], end=' ')
        print(Fore.YELLOW + 'Referer: %s' % entry['referer'], end=' ')
        if entry['status'] != '200':
            print(Fore.WHITE + 'User-Agent: %s' % entry['agent'], end=' ')
        print(Fore.WHITE)
        

