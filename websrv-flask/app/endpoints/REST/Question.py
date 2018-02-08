"""
    All http endpoints that concern the rest-like api for Question
"""

from flask import make_response, g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException, DuplicateQuestionNameException
from framework.flask_request import expect
from framework.internationalization import _
from main import app
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire


@app.route("/api/question", methods=["POST"])
@expect(('questionnaire', str), ('question_group', str), ('text', str))
def api_question_create(questionnaire='', question_group='', text=''):

    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    try:
        the_questionnaire = Questionnaire(questionnaire)
        the_question_group = QuestionGroup(question_group)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)


    try:
        question = the_questionnaire.add_question_to_group(
            the_question_group, text)

    except DuplicateQuestionNameException:
        return make_error(_("A Question with that name already exists."), 400)

    return jsonify({
        "result": _("Question created."),
        "question": question
    })



@app.route("/api/question", methods=["PUT"])
@expect(('uuid', str), ('text', str))
def api_question_update(uuid='', text=''):

    try:
        question = Question(uuid)
        question.text = text

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    return jsonify({
        "result": _("Question updated."),
        "question": Question
    })


@app.route("/api/question", methods=["DELETE"])
@expect(('uuid', str), ('question_group', str), ('questionnaire', str))
def api_question_delete(uuid='', question_group='', questionnaire=''):

    try:
        question = Question(uuid)
        the_question_group = QuestionGroup(question_group)
        the_questionnaire = Questionnaire(questionnaire)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not the_question_group.accessible():
        return make_error(_("Lacking credentials"), 403)

    the_questionnaire.remove_question_from_group(the_question_group, question)
    # TODO: remove all answers to deleted question

    return jsonify({"result": _("Question deleted.")})


@app.route("/api/question/<string:question_uuid>/statistic", methods=["GET"])
def api_question_statistic(question_uuid):
    try:
        question = Question(question_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not question.accessible():
        return make_error(_("Lacking credentials"), 403)

    return jsonify(question.statistic)
