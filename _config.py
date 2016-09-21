# This is a sample config.py file, rename it to config.py

debug_mode = False 
local_debug = False
database_file = 'apache.db'
slack_url = 'https://hooks.slack.com/services/what?'
domain_name = 'http://www.example.com'

url_ignore_list = []
agent_ignore_list = []
cacheable_param = []
host_ignore_list = []


def toggle_debug(status):
    global debug_mode
    debug_mode = status
