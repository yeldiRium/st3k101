import time

from flask import g

from framework.memcached import get_memcache
from model.Question import Question


def lazy_update_statistics():

    key = "STATS_LAST_UPDATE_TIMESTAMP"
    now = time.time()
    mc = get_memcache()
    mc.add(key, now)  # ensure timestamp exists in mc
    last_upate_time = mc.get(key)

    # check if update should happen
    if  now - last_upate_time > g._config["STATISTICS_UPDATE_INTERVAL"]:
        dirty_questions = Question.many_from_query({"dirty": True})
        for question in dirty_questions:
            question.statistics.update()

        mc.set(key, now)


LAZY_JOBS = [lazy_update_statistics]