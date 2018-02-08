"""
    All http endpoints that concern the rest-like api for QuestionGroup
    
"""

from flask import make_response, g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException, DuplicateQuestionGroupNameException
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from main import app
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire


@app.route("/api/question_group", methods=["POST"])
@expect(('questionnaire', str), ('name', str))
def api_questiongroup_create(questionnaire='', name=''):

    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    try:
        the_questionnaire = Questionnaire(questionnaire)
    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    try:
        question_group = the_questionnaire.add_question_group(name)
        the_questionnaire.questiongroups.add(question_group)

    except DuplicateQuestionGroupNameException:
        return make_error(_("QuestionGroup with that name already exists."), 400)

    return jsonify({
        "result": _("QuestionGroup created."),
        "question_group": question_group
    })

@app.route("/api/question_group", methods=["PUT"])
@expect(('uuid', str))
@expect_optional(('name', str), ('color', str), ('text_color', str))
def api_questiongroup_update(uuid='', name=None, color=None, text_color=None):

    try:
        question_group = QuestionGroup(uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    try:
        if name is not None:
            question_group.name = name
        if color is not None:
            question_group.color = color
        if text_color is not None:
            question_group.text_color = text_color

    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)

    return jsonify({
            "result": _("QuestionGroup updated."),
            "question_group": question_group
        })


@app.route("/api/question_group", methods=["DELETE"])
@expect(('uuid', str), ('questionnaire', str))
def api_questiongroup_delete(uuid='', questionnaire=''):

    try:
        question_group = QuestionGroup(uuid)
        the_questionnaire = Questionnaire(questionnaire)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    the_questionnaire.questiongroups.remove(question_group)
    question_group.remove()

    return jsonify({"result": _("QuestionGroup deleted.")})
