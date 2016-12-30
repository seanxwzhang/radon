import re

# Refer to this page for log format
# http://httpd.apache.org/docs/2.4/logs.html

parts = [
        r'(?P<host>\S+)',  # host %h
        r'\S+',  # - % useless
        r'(?P<user>\S+)',  # user id %u
        r'\[(?P<time>.+)\]',  # time %t
        r'"(?P<request>.+)"',  # request line
        r'(?P<status>\d+)',  # status code
        r'(?P<size>\d+)',  # response size
        r'"(?P<referer>.*)"',  # referer
        r'"(?P<agent>.*)"'  # user agent
]
log_pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')


def parse(line):
    m = log_pattern.match(line)
    res = m.groupdict()
    req = res['request'].split(' ')
    res['method'] = req[0]
    res['uri'] = req[1]
    res['version'] = req[2]
    return res
