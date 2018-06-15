"""
This file contains methods for maintenance jobs etc.
"""

from model.SQLAlchemy.models.Question import Question

__author__ = "Noah Hummel, Hannes Leutloff"


def update_dirty_statistics() -> int:
    """
    Helper method to run updates on all QuestionResults that are new since the
    last update.
    :return: int The amount of Questions updated
    """
    dirty_questions = Question.query.filter_by(dirty=True).all()
    counter = 0
    for question in dirty_questions:
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
    questions = Question.query.all()
    counter = 0
    for question in questions:
        question.statistic.update()
        question.dirty = False
        counter = counter + 1

    return counter
