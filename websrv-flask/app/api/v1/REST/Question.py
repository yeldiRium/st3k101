"""
    All http endpoints that concern the rest-like api for Question
"""

from flask.json import jsonify

from app import app
from framework import make_error
from framework.flask_request import expect
from framework.internationalization import _
from framework.ownership import owned
from model.SQLAlchemy import db

from model.SQLAlchemy.models.Question import Question
from model.SQLAlchemy.models.QuestionGroup import QuestionGroup
from view.views.Question import LegacyView
from view.views.QuestionStatistic import LegacyView as QuestionStatistic_LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/question", methods=["POST"])
@expect(
    ('questionnaire_uuid', int),
    ('question_group_uuid', int),
    ('text', str)
)
def api_question_create(
        questionnaire_uuid: int=None,
        question_group_uuid: int=None,
        text: str=None
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

    question_group = QuestionGroup.query.get_or_404(question_group_uuid)
    if question_group.questionnaire_id != questionnaire_uuid:
        return make_error(_("No such QuestionGroup."), 404)

    if not owned(question_group):
        return make_error(_("Lacking credentials."), 403)

    question = Question(text=text)
    question_group.questions.append(question)
    db.session.commit()

    return jsonify({
        "result": _("Question created."),
        "question": LegacyView.render(question)
    })


@app.route("/api/question/<int:question_uuid>", methods=["GET"])
def api_question_get(question_uuid: int):
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
    question = Question.query.get_or_404(question_uuid)
    return LegacyView.jsonify(question)


@app.route("/api/question/<int:question_uuid>", methods=["PUT"])
@expect(('text', str))
def api_question_update(question_uuid: int, text: str=None):
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
    question = Question.query.get_or_404(question_uuid)

    if not owned(question):
        return make_error(_("Lacking credentials."), 403)

    question.text = text
    db.session.commit()

    return jsonify({
        "result": _("Question updated."),
        "question": LegacyView.render(question)
    })


@app.route("/api/question/<int:question_uuid>", methods=["DELETE"])
@expect(
    ('question_group_uuid', int),
    ('questionnaire_uuid', int)
)
def api_question_delete(
        question_uuid: int,
        question_group_uuid: int=None,
        questionnaire_uuid: int=None
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
    question = Question.query.get_or_404(question_uuid)

    if question.question_group_id != question_group_uuid:
        return make_error(_("No such Question."), 404)
    elif question.question_group.questionnaire_id != questionnaire_uuid:
        return make_error(_("No such Question."), 404)
    elif not owned(question):
        return make_error(_("Lacking credentials."), 403)

    db.session.delete(question)
    db.session.commit()

    return jsonify({"result": _("Question deleted.")})


@app.route("/api/question/<int:question_uuid>/statistic", methods=["GET"])
def api_question_statistic(question_uuid: int):
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
    question = Question.query.get_or_404(question_uuid)

    if not owned(question):
        return make_error(_("Lacking credentials"), 403)

    return QuestionStatistic_LegacyView.jsonify(question.statistic)
