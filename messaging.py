# Radon Project
# Created by Xinyu Chen
# Modified by Xiaowen Zhang

# messaging.py
# Messaging Subsystem
# This module handles all messaging and notification service in the following way
# 1. Push all incoming message to a queue
# 2. Open another thread as a consumer 
# 3. The consumer checks the queue every n seconds
# 4. The consumer aggregates all possible message, determined by the same resources requested and status code
# 5. The consumer sends the first K messages to Slack, storing them and the rest in a static url

import config
import requests
import utils
import queue
import threading
import os
from time import sleep
from datetime import datetime

slack_enabled = False
json_payload = '{{"text": "{0}"}}'


def send_slack_message(message):
    if not message_queue.full():
        message_queue.put(message)
    else: # if the queue is full, pop the first message in a log file
        poped_message = message_queue.get()
        dir = os.getcwd()
        with open(dir + "/log/system.log", "a") as system_log:
            system_log.write(poped_message + "\n")
        utils.print_debug("WARNING: message queue FULL!")
        send_message("WARNING: message queue FULL!\n")


def send_message(message):
    if not slack_enabled:
            return
    payload = json_payload.format(message)
    response = requests.post(config.slack_url, data=payload)
    utils.print_debug('Slack message sent {0}'.format(payload))
    if response.status_code != 200:
        utils.print_error('Failed to sent slack message: {0}'.format(payload))


def consume_message():
    if message_queue.empty():
        return
    message = message_queue.get()
    send_message(message)


def toggle_slack_message(status):
    global slack_enabled
    utils.print_debug('slack is toggled to %s' % status)
    if status == '0':
        slack_enabled = False
    elif status == '1':
        slack_enabled = True


def add_to_email_queue(content):
    if config.debug_mode:
        utils.print_debug('DEBUG: Added to email queue: %s' % content)
    message_queue.put()


def send_emails():
    pass


def worker(threshold=None, time_gap=None): # An ascync worker program to consume the queue
    if threshold is None:
        threshold = 5
    if time_gap is None:
        time_gap = 30
    while True:
        # print("Worker wakes up\n")
        length = message_queue.qsize();
        # print("Current message queue has {0} message".format(length))
        to_consume = min(length, threshold)
        for i in range(0, to_consume):
            consume_message()
        if (length > threshold): # store the rest into a message file
            dir = os.getcwd()
            with open(dir + "/log/message.store", "a") as msg_store:
                for i in range(threshold, length):
                    message = message_queue.get()
                    msg_store.write("[{0}] Stored message: {1}\n".format(datetime.now(), message))
        sleep(time_gap)


message_queue = queue.Queue(maxsize = config.max_message_size)
try:
    worker_thread = threading.Thread( target = worker, args = (config.queue_threshold, config.time_gap) )
    worker_thread.start()
except:
    print("Error: unable to start worker thread")

