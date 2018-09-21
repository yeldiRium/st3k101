import time
from flask import g
from framework.memcached import get_memcache
from .services import update_dirty_statistics

__author__ = "Noah Hummel, Hannes Leutloff"


def lazy_update_statistics() -> None:
    """
    A helpfer function to run updates of the statistics module deferred and
    not every time a new result comes in.
    :return: None
    """
    key = "STATS_LAST_UPDATE_TIMESTAMP"
    now = time.time()
    mc = get_memcache()
    mc.add(key, now)
    last_update_time = mc.get(key)

    # check if update should happen
    if now - last_update_time > g._config["STATISTICS_UPDATE_INTERVAL"]:
        update_dirty_statistics()
        mc.set(key, now)


# a list of all functions that should be run on every request
LAZY_JOBS = []  # [lazy_update_statistics]
