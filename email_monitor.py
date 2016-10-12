# Email Queue Monitor
# Monitor the email queue to check whether the queue is congested due to invalid entries.
# This is just a workaround solution. But I believe this module can be expanded into a general database monitor

import config
import json
import messages
import pymysql
from datetime import datetime


def serialize_datetime(dt):
    return dt.isoformat() + 'Z'     # TODO convert to local time

slack_message = "A possible email queue block is detected.\nRecipient email: {0}\nRecipient name: {1}"

connection = pymysql.connect(host=config.mysql_host,
                             user=config.mysql_username,
                             password=config.mysql_password,
                             db=config.mysql_database,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql_select = 'SELECT * FROM core_email_queue WHERE processed_at IS NULL ORDER BY created_at'
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            created_at = row['created_at']
            current = datetime.now()
            if (current - created_at).total_seconds() > config.delay_interval:
                data = {'email': row}
                sql_select = 'SELECT * FROM core_email_queue_recipients WHERE message_id = %s'
                cursor.execute(sql_select, (row['message_id'],))
                recipient = cursor.fetchone()
                if recipient is not None:
                    data['recipient'] = recipient
                    sql_delete = 'DELETE FROM core_email_queue_recipients WHERE message_id = %s'
                    cursor.execute(sql_delete, (row['message_id'],))
                    messages.send_slack_message(
                        slack_message.format(recipient['recipient_email'], recipient['recipient_name']))
                sql_delete = 'DELETE FROM core_email_queue WHERE message_id = %s'
                cursor.execute(sql_delete, (row['message_id'],))
                connection.commit()
                log_file = open(config.log_path + 'email_' + str(row['message_id']) + '.log', 'w')
                json.dump(data, log_file, indent='\t', default=serialize_datetime)
                exit(0)
finally:
    connection.close()
