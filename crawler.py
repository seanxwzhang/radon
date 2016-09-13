# A multi-thread crawler for rebuilding website cache
# Originally written by Tianyang Wen
# Modified by Xinyu Chen

import queue
import requests
import config
import dbo
from threading import Thread


def crawler(arguments):
    global url_queue
    thread_id = arguments
    print("Thread No. {0} has started.".format(thread_id))
    while True:
        url = url_queue.get()
        if url is None:
            break
        get_url(url)
        url_queue.task_done()


def get_url(url):
    headers = {'user-agent': 'radon/0.0.1'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            dbo.delete_visited_url(url)
            print("404: {0}".format(url))
        elif response.status_code == 200:
            print("200: {0}".format(url))
    except requests.exceptions.ConnectionError:
        print("Err: {0}".format(url))


url_queue = queue.Queue()
threads = []
num_threads = 1
base_url = config.domain_name
for i in range(num_threads):
    t = Thread(target=crawler, args=(i,))
    t.start()
    threads.append(t)

urls = dbo.get_visit_stats()
for u in urls:
    url_queue.put(base_url + u)

url_queue.join()
for i in range(num_threads):
    url_queue.put(None)
for t in threads:
    t.join()
