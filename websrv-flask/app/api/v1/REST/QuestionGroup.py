"""
    All http endpoints that concern the rest-like api for QuestionGroup
    
"""

from flask.json import jsonify

from app import app
from framework import make_error
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from framework.ownership import owned
from model.SQLAlchemy import db

from model.SQLAlchemy.models.QuestionGroup import QuestionGroup
from model.SQLAlchemy.models.Questionnaire import Questionnaire
from view.views.QuestionGroup import LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/question_group", methods=["POST"])
@expect(('questionnaire_uuid', int), ('name', str))
def api_questiongroup_create(questionnaire_uuid: int=None, name: str=''):
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

    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not owned(questionnaire):
        return make_error(_("Lacking credentials"), 403)

    question_group = QuestionGroup(name=name)
    questionnaire.question_groups.append(question_group)
    db.session.commit()

    return jsonify({
        "result": _("QuestionGroup created."),
        "question_group": LegacyView.render(question_group)
    })


@app.route("/api/question_group/<int:question_group_uuid>", methods=["GET"])
def api_questiongroup_get(question_group_uuid: int=None):
    """
    Parameters:
        question_group_uuid: String The uuid for the QuestionGroup to retrieve.

    Response Codes:
        200: QuestionGroup is returned.
        404: The question_group_uuid doesn't belong to a valid QuestionGroup.

    Response Class:
        200:  QuestionGroup {
            "class": "model.QuestionGroup.QuestionGroup",
            "fields": {
                "color": String,
                "name": {
                    "class": "model.I15dString.I15dString",
                    "fields": {
                        "default_locale": language_shorthand: String,
                        "locales": {
                            language_shorthand: question_group_name: String
                        }
                    },
                    "uuid": String
                },
                "questions": [Question], (see GET /api/question/question_uuid)
                "text_color": String
            },
            "uuid": String
        }
        404: {
            "error": "No such QuestionGroup.",
            "result": "error"
        }
    """
    question_group = QuestionGroup.query.get_or_404(question_group_uuid)
    return LegacyView.jsonify(question_group)


@app.route("/api/question_group/<int:question_group_uuid>", methods=["PUT"])
@expect_optional(('name', str), ('color', str), ('text_color', str))
def api_questiongroup_update(
        question_group_uuid: int=None,
        name: str=None,
        color: str=None,
        text_color: str=None
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
    question_group = QuestionGroup.query.get_or_404(question_group_uuid)

    if not owned(question_group):
        return make_error(_("Lacking credentials"), 403)

    if name is not None:
        question_group.name = name

    try:
        if color is not None:
            question_group.set_color(color)
        if text_color is not None:
            question_group.set_text_color(text_color)
    except ValueError as e:
        return make_error(
            _("Parameter malformed: {}".format(e.args[0])),
            400
        )

    db.session.commit()
    return jsonify({
            "result": _("QuestionGroup updated."),
            "question_group": LegacyView.render(question_group)
        })


@app.route("/api/question_group/<int:question_group_uuid>", methods=["DELETE"])
@expect(('questionnaire_uuid', int))
def api_questiongroup_delete(question_group_uuid: int=None,
                             questionnaire_uuid: int=None):
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
    question_group = QuestionGroup.query.get_or_404(question_group_uuid)

    if question_group.questionnaire_id != questionnaire_uuid:
        return make_error(_("No such QuestionGroup."), 404)

    if not owned(question_group):
        return make_error(_("Lacking credentials"), 403)

    db.session.delete(question_group)
    db.session.commit()

    return jsonify({"result": _("QuestionGroup deleted.")})
