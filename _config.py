# This is a sample config.py file, rename it to config.py

debug_mode = False 
local_debug = False
database_file = 'apache.db'
slack_url = 'https://hooks.slack.com/services/what?'
domain_name = 'http://www.example.com'

# email monitor parameters
mysql_username = ''
mysql_password = ''
mysql_host = '127.0.0.1'
mysql_database = ''
check_interval = 600    # seconds
delay_interval = 300    # seconds
log_path = './log/'

# message parameters
max_message_size = 10   # maximum number of messages the queue can hold
queue_threshold = 5     # maximum number of messsages one thread coudl consume at a time
time_gap = 30           # seconds

# monitor parameters
url_ignore_list = []
agent_ignore_list = []
cacheable_param = []
host_ignore_list = []

# Log related
log_file_path = './log/system.log'


def toggle_debug(status):
    global debug_mode
    debug_mode = status
