import time

from flask import g

from framework.memcached import get_memcache
from model.Question import Question


def lazy_update_statistics():
    """
    A helpfer function to run updates of the statistics module deferred and
    not every time a new result comes in.
    :return: None
    """

    key = "STATS_LAST_UPDATE_TIMESTAMP"
    now = time.time()
    mc = get_memcache()
    mc.add(key, now)  # ensure timestamp exists in mc
    last_upate_time = mc.get(key)

    # check if update should happen
    if  now - last_upate_time > g._config["STATISTICS_UPDATE_INTERVAL"]:
        dirty_questions = Question.many_from_query({"dirty": True})
        for question in dirty_questions:
            # only update a question statistic when the owner of the question
            # made the request.
            if not g._current_user:
                continue
            if question.owner_uuid != g._current_user.uuid:
                continue
            question.statistic.update()
            question.dirty = False

        mc.set(key, now)

# a list of all functions that should be run on every request
LAZY_JOBS = [lazy_update_statistics]