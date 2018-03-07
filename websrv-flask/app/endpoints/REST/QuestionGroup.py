"""
    All http endpoints that concern the rest-like api for QuestionGroup
    
"""

from flask import g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from main import app
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire


@app.route("/api/question_group", methods=["POST"])
@expect(('questionnaire_uuid', str), ('name', str))
def api_questiongroup_create(questionnaire_uuid='', name=''):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire on which to create
            a new QuestionGroup.
        name: String The name for the new QuestionGroup.

    Response Codes:
        200: QuestionGroup is successfully created.
        403: No user is logged in or the current user doesn't have permission
            to create a QuestionGroup on the given Questionnaire.
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: {
            "question_group": QuestionGroup (see GET
                /api/question_group/question_group_uuid)
            "result": "QuestionGroup created."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire.",
            "result": "error"
        }
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    try:
        the_questionnaire = Questionnaire(questionnaire_uuid)
    except ObjectDoesntExistException:
        return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    question_group = the_questionnaire.add_question_group(name)

    return jsonify({
        "result": _("QuestionGroup created."),
        "question_group": question_group
    })


@app.route("/api/question_group/<question_group_uuid>", methods=["PUT"])
@expect_optional(('name', str), ('color', str), ('text_color', str))
def api_questiongroup_update(
        question_group_uuid='',
        name=None,
        color=None,
        text_color=None
):
    """
    Parameters:
        question_group_uuid: String The uuid for the QuestionGroup that shall be
            updated.
        name: String The new name for the QuestionGroup.
        color: String A color value for the background. Hex-format, beginning
            with #.
        text_color: String A color value for the text. Hex-format, beginning
            with #.

    Response Codes:
        200: QuestionGroup is successfully updated.
        400: Color values are not formatted correctly.
        403: No user is logged in or the current user doesn't have permission
            to create a QuestionGroup on the given Questionnaire.
        404: The question_group_uuid doesn't belong to a valid QuestionGroup.

    Response Class:
        200: {
            "question_group": QuestionGroup (see GET
                /api/question_group/question_group_uuid)
            "result": "QuestionGroup updated."
        }
        400:    {
            "error": "Parameter malformatted: '{color}' is not a well formatted color
                value. It must be a hex-string beginning with #.",
            "result": "error"
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire.",
            "result": "error"
        }
    """
    try:
        question_group = QuestionGroup(question_group_uuid)

    except ObjectDoesntExistException:
        return make_error(_("No such QuestionGroup."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)

    try:
        if name is not None:
            question_group.set_name(name)
        if color is not None:
            question_group.set_color(color)
        if text_color is not None:
            question_group.text_color = text_color
    except ValueError as e:
        return make_error(
            _("Parameter malformatted: {}".format(e.args[0])),
            400
        )
    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)

    return jsonify({
            "result": _("QuestionGroup updated."),
            "question_group": question_group
        })


@app.route("/api/question_group/<string:question_group_uuid>", methods=["DELETE"])
@expect(('questionnaire_uuid', str))
def api_questiongroup_delete(question_group_uuid='', questionnaire_uuid=''):
    """
    Parameters:
        question_group_uuid: String The uuid for the QuestionGroup to delete.
        questionnaire_uuid: String The uuid for the Questionnaire on which to delete
            the QuestionGroup.

    Response Codes:
        200: QuestionGroup is successfully deleted.
        403: No user is logged in or the current user doesn't have permission
            to delete the given QuestionGroup.
        404: The question_group_uuid or questionnaire_uuid doesn't belong to a
            valid object.

    Response Class:
        200: {
            "result": "QuestionGroup deleted."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such QuestionGroup." / "No such Questionnaire.",
            "result": "error"
        }
    """
    try:
        question_group = QuestionGroup(question_group_uuid)
        the_questionnaire = Questionnaire(questionnaire_uuid)

    except ObjectDoesntExistException as e:
        if e.args[1] is "QuestionGroup":
            return make_error(_("No such QuestionGroup."), 404)
        else:
            return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    the_questionnaire.remove_question_group(question_group)

    return jsonify({"result": _("QuestionGroup deleted.")})
