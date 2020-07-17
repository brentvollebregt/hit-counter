import time
import math
from threading import Lock, Timer

from prometheus_client import Gauge

import config

METRICS_PREFIX = config.METRICS_PREFIX
CACHE_TIMEOUT_SEC = 5
REGISTER_INTERVAL_SEC = 120

cached_data = None
last_fetched = 0
lock = Lock()


def init_metrics(db_connection):
    g = Gauge(f'{METRICS_PREFIX}_hits_total', 'Total number of hits', ['site', 'path'])
    register_labels(db_connection, g)

    Timer(REGISTER_INTERVAL_SEC, lambda: register_labels(db_connection, g)).start()


def register_labels(db_connection, gauge):
    url_counts = db_connection.getTopUrls(db_connection.get_connection(), -1)
    for url in url_counts['urls']:
        site, path = _split_url(url)
        gauge.labels(site, path).set_function(_get_resolver(db_connection, site, path))


def resolve_label_count(db, site, path):
    global lock, cached_data, last_fetched

    lock.acquire()

    if time.monotonic() - last_fetched >= CACHE_TIMEOUT_SEC:
        cached_data = db.getTopUrls(db.get_connection(), -1)
        last_fetched = time.monotonic()

    url = f'{site}/{path}'
    if url not in cached_data['values']:
        lock.release()
        return 0

    lock.release()
    return cached_data['values'][url]


def _split_url(url):
    split = url.split('/')
    return split[0], '/'.join(split[1:])


def _get_resolver(db, for_site, for_path):
    def call():
        return resolve_label_count(db, for_site, for_path)

    return call
