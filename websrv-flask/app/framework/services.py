from flask import g
from model.Question import Question


def update_dirty_statistics():
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
