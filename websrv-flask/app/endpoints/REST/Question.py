"""
    All http endpoints that concern the rest-like api for Question
"""

from flask import g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException
from framework.flask_request import expect
from framework.internationalization import _
from app import app
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/question", methods=["POST"])
@expect(
    ('questionnaire_uuid', str),
    ('question_group_uuid', str),
    ('text', str)
)
def api_question_create(
        questionnaire_uuid: str=None,
        question_group_uuid: str=None,
        text: str =None
):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire on which to
            create the Question.
        question_group_uuid: String The uuid for the QuestionGroup on which to
            create the Question.
        text: String The default text for the question.

    Response Codes:
        200: The Question is successfully created on the given Hierarchy.
        403: No user is logged in or the current user doesn't have permission
            to create a Question on the given hierarchy.
        404: The questionnaire_uuid or question_group_uuid doesn't belong to a
            valid object.

    Response Class:
        200: {
            "question": Question (see GET /api/question/question_uuid),
            "result": "Question created."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such QuestionGroup.",
            "result": "error"
        }
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    try:
        the_questionnaire = Questionnaire(questionnaire_uuid)
        the_question_group = QuestionGroup(question_group_uuid)
    except ObjectDoesntExistException as e:
        if e.args[1] is "Questionnaire":
            return make_error(_("No such Questionnaire."), 404)
        else:
            return make_error(_("No such QuestionGroup."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    question = the_questionnaire.add_question_to_group(
        the_question_group, text)

    return jsonify({
        "result": _("Question created."),
        "question": question
    })


@app.route("/api/question/<string:question_uuid>", methods=["GET"])
def api_question_get(question_uuid: str):
    """
    Parameters:
        question_uuid: String The uuid for the Question to retrieve.

    Response Codes:
        200: The Question is returned.
        404: The uuid doesn't belong to a valid Question.

    Response Class:
        200: Question: {
                "class": "model.Question.Question",
                "fields": {
                    "text": {
                        "class": "model.I15dString.I15dString",
                        "fields": {
                            "default_locale": language_shorthand: String,
                            "locales": {
                                language_shorthand: question_text: String
                            }
                        },
                        "uuid": String
                    }
                },
                "uuid": String
            }
        404: {
            "error": "No such Question.",
            "result": "error"
        }
    """
    try:
        question = Question(question_uuid)
    except ObjectDoesntExistException:
        return make_error(_("No such Question."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    return jsonify(question)


@app.route("/api/question/<string:question_uuid>", methods=["PUT"])
@expect(('text', str))
def api_question_update(question_uuid: str, text: str=None):
    """
    Parameters:
        question_uuid: String The uuid for the Question to update.
        text: String The new text for the Question.

    Updates the Text in the currently set language for the given Question.
    I.e. if the Question in question already has a german text but none in eng-
    lish and the currently set language is english, a new language with the gi-
    ven text is added.

    Response Codes:
        200: The Question is updated.
        403: No user is logged in or the current user doesn't have permission
            to update the Question in question.
        404: The uuid doesn't belong to a valid Question.

    Response Class:
        200: {
            "question": Question (see GET /api/question/question_uuid)
            },
            "result": "Question updated."
        }
        403: {
            "error": "Lacking credentials.",
            "result": "error"
        }
        404: {
            "error": "No such Question.",
            "result": "error"
        }
    """
    try:
        question = Question(question_uuid)
        question.update_text(text)
    except ObjectDoesntExistException:
        return make_error(_("No such Question."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not question.accessible():
        return make_error(_("Lacking credentials"), 403)

    return jsonify({
        "result": _("Question updated."),
        "question": question
    })


@app.route("/api/question/<string:question_uuid>", methods=["DELETE"])
@expect(
    ('question_group_uuid', str),
    ('questionnaire_uuid', str)
)
def api_question_delete(
        question_uuid: str,
        question_group_uuid: str=None,
        questionnaire_uuid: str=None
):
    """
    Parameters:
        question_uuid: String The uuid for the Question to delete.
        question_group_uuid: String The uuid for the QuestionGroup on which to
            delete the Question.
        questionnaire_uuid: String The uuid for the Questionnaire on which to
            delete the Question.

    Response Code:
        200: The Question is deleted successfully.
        403: No user is logged in or the current user doesn't have permission
            to delete the Question in question.
        404: The uuid, question_group_uuid or questionnaire_uuid doesn't belong
            to a valid object.

    Response Class:
        200: {
            "result": "Question deleted."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Question." / "No such Questionnaire."
                / "No such QuestionGroup.",
            "result": "error"
        }
    """
    try:
        question = Question(question_uuid)
        the_question_group = QuestionGroup(question_group_uuid)
        the_questionnaire = Questionnaire(questionnaire_uuid)
    except ObjectDoesntExistException as e:
        if e.args[1] is "Question":
            return make_error(_("No such Question."), 404)
        elif e.args[1] is "Questionnaire":
            return make_error(_("No such Questionnaire."), 404)
        else:
            return make_error(_("No such QuestionGroup."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not the_questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    the_questionnaire.remove_question_from_group(the_question_group, question)

    return jsonify({"result": _("Question deleted.")})


@app.route("/api/question/<string:question_uuid>/statistic", methods=["GET"])
def api_question_statistic(question_uuid: str):
    """
    Parameters:
        question_uuid: String The uuid for the Question to retrieve the statis-
            tics for.

    Response Code:
        200: The QuestionStatistic is returned.
        403: No user is logged in or the current user doesn't have permission
            to retrieve the QuestionStatistic in question.
        404: The uuid, question_group_uuid or questionnaire_uuid doesn't belong
            to a valid object.

    Response Class:
        200: {
            "class": "model.QuestionStatistic.QuestionStatistic",
            "fields": {
                "biggest": Double / null,
                "q1": Double / null,
                "q2": Double / null,
                "q3": Double / null,
                "smallest": Double / null
            },
            "uuid": String
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Question.",
            "result": "error"
        }
    """
    try:
        question = Question(question_uuid)

    except ObjectDoesntExistException:
        return make_error(_("Not found."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)

    if not question.accessible():
        return make_error(_("Lacking credentials"), 403)

    return jsonify(question.statistic)
