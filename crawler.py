# A multi-thread crawler for rebuilding website cache
# Originally written by Tianyang Wen, modified by Xinyu Chen

# Command line arguments
# crawler num_threads base_url
# num_threads defaults to 8
# base_url defaults to database value

import queue
import requests
import config
import dbo
import sys
import time
from threading import Thread


def crawler(arguments):
    """ The crawler thread function"""
    global url_queue
    thread_id = arguments
    print("Thread {0} has started.".format(thread_id))
    while True:
        if url_queue.empty():
            break
        url = url_queue.get()
        get_url(url)
        url_queue.task_done()


def get_url(url):
    global bad_urls
    headers = {'user-agent': 'radon/0.0.1'}
    try:
        t_start = time.time()
        response = requests.get(url, headers=headers)
        t_end = time.time()
        if response.status_code == 404:
            bad_urls.put(url)
            print("HTTP 404: {0}".format(url))
        elif response.status_code == 200:
            print("HTTP 200 Time: {0:6.3f} s {1}".format(t_end - t_start, url))
    except requests.exceptions.ConnectionError:
        print("Err: {0}".format(url))
        bad_urls.put(url)


"""Here comes the main part"""
num_threads = 8
base_url = config.domain_name
if len(sys.argv) >= 2:
    num_threads = int(sys.argv[1])
if len(sys.argv) >= 3:
    base_url = sys.argv[2]
url_queue = queue.Queue()
bad_urls = queue.Queue()
threads = []
urls = dbo.get_visit_stats()
for u in urls:
    url_queue.put(base_url + u)

for i in range(num_threads):
    t = Thread(target=crawler, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
