#!/usr/bin/python3

# Import data into the database

import logparser
import httpagentparser
import json
import re
import sqlite3

from datetime import datetime

conn = None
if conn is None:
    conn = sqlite3.connect('/home/xinyu/src/radon/db.sqlite3')


def find_host(host):
    cur = conn.cursor()
    sql_select = 'SELECT * FROM apache_monitor_remotehost WHERE ip_address = ?'
    ret = cur.execute(sql_select, (host,))
    res = ret.fetchall()
    if len(res) == 0:
        sql_insert = "INSERT INTO apache_monitor_remotehost" \
                     "(`ip_address`) VALUES ( ? )"
        cur.execute(sql_insert, (host,))
        conn.commit()
        ret = cur.execute(sql_select, (host,))
        res = ret.fetchall()
    return res[0][0]    # id


def find_request_uri(uri):
    cur = conn.cursor()
    sql_select = 'SELECT * FROM apache_monitor_requesteduri WHERE uri = ?'
    ret = cur.execute(sql_select, (uri,))
    res = ret.fetchall()
    if len(res) == 0:
        sql_insert = "INSERT INTO apache_monitor_requesteduri" \
                     "(`uri`,  `visit_count`, `should_crawl`) VALUES" \
                     "( ?, 1, 0)"
        cur.execute(sql_insert, (uri,))
        conn.commit()
        ret = cur.execute(sql_select, (uri,))
        res = ret.fetchall()
    return res[0][0]


def find_search_engine(user_agent):
    return -1   # I don't really know how to figure out whether it is a search engine based on user agent


def find_referer(referer):
    cur = conn.cursor()
    sql_select = 'SELECT * FROM apache_monitor_referer WHERE url = ?'
    ret = cur.execute(sql_select, (referer,))
    res = ret.fetchall()
    if len(res) == 0:
        slashes = [m.start() for m in re.finditer(r'/', referer)]
        internal_uri = ''
        if len(slashes) < 3:
            print("No referer")
        else:
            internal_uri = referer[slashes[2]:]
        internal_uri_id = find_request_uri(internal_uri)
        sql_insert = "INSERT INTO apache_monitor_referer" \
                     "(`url`, `internal_uri_id`) VALUES" \
                     "(?, ?)"
        cur.execute(sql_insert, (referer, internal_uri_id))
        conn.commit()
        ret = cur.execute(sql_select, (referer,))
        res = ret.fetchall()
    return res[0][0]


def find_user_agent(user_agent):
    res = httpagentparser.simple_detect(user_agent)
    sql_insert = "INSERT OR IGNORE INTO apache_monitor_useragent" \
                 "(`operating_system`, `browser`) VALUES" \
                 "(?, ?)"
    cur = conn.cursor()
    cur.execute(sql_insert, res)
    sql_select = 'SELECT * FROM apache_monitor_useragent WHERE operating_system = ? AND browser = ?'
    ret = cur.execute(sql_select, res)
    return ret.fetchone()[0]


def insert_log_entry(entry):
    ts = datetime.strptime(entry['time'], "%m/%b/%Y:%H:%M:%S %z").timestamp()
    host_id = find_host(entry['host'])
    uri_id = find_request_uri(entry['uri'])
    referer_id = find_referer(entry['referer'])
    user_agent_id = find_user_agent(entry['agent'])
    status_code = entry['status']
    cur = conn.cursor()
    sql_insert = "INSERT INTO apache_monitor_logentry" \
                 "(`status_code`, `referer_id`, `remote_host_id`, " \
                 "`requested_uri_id`, `user_agent_id`, `method`, `timestamp`) VALUES" \
                 "(?, ?, ?, ?, ?, ?, ?)"
    cur.execute(sql_insert, (status_code, referer_id, host_id, uri_id, user_agent_id, entry['method'], ts))
    conn.commit()


log_file = open('access.log', 'r')
count = 1
for line in log_file:
    entry = logparser.parse(line)
    insert_log_entry(entry)
    print(count)
    count += 1


