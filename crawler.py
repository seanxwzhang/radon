# A multi-thread crawler for rebuilding website cache
# Originally written by Tianyang Wen, modified by Xinyu Chen

# Command line arguments
# crawler num_threads base_url
# num_threads defaults to 8
# base_url defaults to database value

import argparse
import queue
import requests
import dbo
import time
import threading


def get_url_list(arguments):
    if arguments.file is None:
        entries = dbo.get_visit_stats()
        url_list = [arguments.base_url + entry for entry in entries]
    else:
        url_file = open(args.file, 'r')
        url_list = [u.rstrip() for u in url_file]
    return url_list


def crawler(arguments):
    """ The crawler thread function"""
    global url_queue
    thread_id = arguments
    print("Thread {0} has started.".format(thread_id))
    while True:
        if url_queue.empty():
            break
        u = url_queue.get()
        url_queue.task_done()
        crawl(u)


def crawl(url):
    global bad_urls
    global time_stats
    headers = {'user-agent': 'radon/0.0.1'}
    try:
        t_start = time.time()
        response = requests.get(url, headers=headers)
        t_end = time.time()
        if response.status_code == 200:
            print("HTTP 200 Time: {0:6.3f}s {1}".format(t_end - t_start, url))
            time_stats.put(t_end - t_start)
        else:
            bad_urls.put("HTTP {0}: {1}; time {2}".format(response.status_code, url, t_end - t_start))
    except requests.exceptions.ConnectionError:
        bad_urls.put("Connection Error: {0}".format(url))


"""Here comes the main part"""

parser = argparse.ArgumentParser(description='A multi-threaded crawler for rapid cache rebuild.')
parser.add_argument('-b', '--base_url', help='Base URL, only needed for data from database. Default to '
                                             'http：//www.evestemptation.com. Don\'t add the trailing slash /',
                    default='http://www.evestemptation.com')
parser.add_argument('-f', '--file', help='file name from which the URL list is read')
parser.add_argument('-t', '--threads', help='Number of threads to crawl. Default to 12.', type=int, default=12)
args = parser.parse_args()
mutex = threading.Lock
url_queue = queue.Queue()
bad_urls = queue.Queue()
time_stats = queue.Queue()
threads = []
urls = get_url_list(args)
for url in urls:
    url_queue.put(url)
for i in range(args.threads):
    t = threading.Thread(target=crawler, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

min_time = 1000.0
max_time = 0.0
total_time = 0.0
total_count = 0
while not time_stats.empty():
    t = time_stats.get()
    total_time += t
    total_count += 1
    min_time = min([min_time, t])
    max_time = max([max_time, t])
ave_time = total_time / total_count
print('=== Stats ===')
print('\tTotal URLs crawled: {0}'.format(total_count))
print('\tAverage response time: {0}'.format(ave_time))
print('\tShortest response time: {0}'.format(min_time))
print('\tLongest response time: {0}'.format(max_time))
print('=== Error URLs ===')
while not bad_urls.empty():
    print(bad_urls.get())
print('Crawler is done!')

