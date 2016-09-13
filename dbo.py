import time
import re
import sqlite3

import config


conn = None

if conn is None:
    conn = sqlite3.connect(config.database_file)
else:
    raise RuntimeError('Database connection already established.')


def destroy():
    conn.close()


def add_ignore_url(url):
    cur = conn.cursor()
    sql = 'INSERT OR IGNORE INTO `url_ignore_list` (pattern) VALUES (?)'


# (Re)load host ignore list
def load_string_list(table_name, column_name):
    cur = conn.cursor()
    sql = 'SELECT {0} FROM {1} WHERE 1'
    cur.execute(sql.format(column_name, table_name))
    rows = cur.fetchall()
    ignore_host = [row[0] for row in rows]
    cur.close()
    return ignore_host


def load_pattern_list(table_name, column_name):
    cur = conn.cursor()
    sql = 'SELECT {0} FROM {1} WHERE 1'  # not sure if this will cause potential SQL injection
    cur.execute(sql.format(column_name, table_name))
    rows = cur.fetchall()
    the_list = [row[0] for row in rows]
    pattern = re.compile(r'(%s)' % r'|'.join(the_list))
    cur.close()
    return pattern


# Store visited URL into the database
def store_visited_url(url):
    sql_insert = "INSERT OR IGNORE INTO url_stats (url, rate) VALUES (?, 0)"
    sql_update = "UPDATE url_stats SET rate = rate + 1 WHERE url = ?"
    cur = conn.cursor()
    cur.execute(sql_insert, (url,))
    cur.execute(sql_update, (url,))
    conn.commit()
    cur.close()
    if config.debug_mode:
        print('DEBUG: {0}({1})'.format(store_visited_url.__name__, url))


def store_error_request(entry):
    sql = "INSERT INTO abnormal_request " \
          "(`timestamp`, `host`, `method`, `status`, `url`, `referer`, `agent`) " \
          "VALUES (?, ?, ?, ?, ?, ?, ?)"
    req = entry['request'].split()
    if len(req) < 3:
        method = req[0]
        url = ''
    else:
        method = req[0]
        url = req[1]
    cur = conn.cursor()
    cur.execute(sql, (
        int(time.time()),
        entry['host'],
        method,
        int(entry['status']),
        url,
        entry['referer'],
        entry['agent']
    ))
    conn.commit()
    cur.close()


def get_visit_stats():
    sql = "SELECT url FROM url_stats WHERE 1 ORDER BY rate DESC"
    cur = conn.cursor()
    ret = cur.execute(sql)
    stats = [u[0] for u in ret]
    return stats


def delete_visited_url(url):
    sql = "DELETE FROM url_stats WHERE url = ?"
    cur = conn.cursor()
    cur.execute(sql, (url,))
    conn.commit()
    cur.close()


def get_email_recipients():
    sql = "SELECT email FROM email_recipients WHERE 1"
    cur = conn.cursor()
    ret = cur.execute(sql)
    rec = [r[0] for r in ret]
    return rec
