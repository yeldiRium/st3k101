"""
This file contains methods for maintenance jobs etc.
"""

from flask import g
from model.Question import Question

__author__ = "Noah Hummel, Hannes Leutloff"


def update_dirty_statistics() -> int:
    """
    Helper method to run updates on all QuestionResults that are new since the
    last update.
    :return: int The amount of Questions updated
    """
    dirty_questions = Question.many_from_query({"dirty": True})
    counter = 0
    for question in dirty_questions:
        # only update a question statistic when the owner of the question
        # made the request.
        if not g._current_user:
            continue
        if question.owner_uuid != g._current_user.uuid:
            continue
        question.statistic.update()
        question.dirty = False
        counter = counter + 1

    return counter

def update_all_statistics() -> int:
    """
    Helper method to update all the statistics. 
    Useful for forcing an update after changing algorithms.
    :return: int The amount of Questions updated
    """
    questions = Question.many_from_query({})
    counter = 0
    for question in questions:
        # only update a question statistic when the owner of the question
        # made the request.
        if not g._current_user:
            continue
        if question.owner_uuid != g._current_user.uuid:
            continue
        question.statistic.update()
        question.dirty = False
        counter = counter + 1

    return counter
