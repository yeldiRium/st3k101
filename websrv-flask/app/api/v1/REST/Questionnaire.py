"""
    All http endpoints that concern the rest-like api for Questionnaire
    
    Note that some endpoints for QAC also start with '/api/questionnaire'.
    These endpoints can be found in QAC.py
"""
import csv
import io
from typing import Any

from flask import make_response
from flask.json import jsonify

from app import app
from framework import make_error
from framework.exceptions import ObjectDoesntExistException
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from framework.ownership import owned
from model.SQLAlchemy import db

from model.SQLAlchemy.models.Questionnaire import Questionnaire
from model.SQLAlchemy.models.Survey import Survey
from view.views.Questionnaire import LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/questionnaire", methods=["POST"])
@expect(
    ('survey_uuid', int),
    ('questionnaire', Any)
)
def api_questionnaire_create(survey_uuid: int=None, questionnaire: Any=None):
    """
    Parameters:
        survey_uuid: String The uuid for the Survey to create a Questionnaire
            on.
        questionnaire: Object A JSON object with different parameters for the
            Questionnaire.

    Response Codes:
        200: Questionnaire is successfully created.
        400: Some parameter is missing. Only questionnaire.name and
            questionnaire.description are required. The API doesn't tell you,
            which one is missing.
        403: No user is logged in or the current user doesn't have permission
            to create a Questionnaire on the given Survey.
        404: The survey_uuid doesn't belong to a valid Survey.

    Response Class:
        200: {
            "questionnaire": Questionnaire (see GET
                /api/questionnaire/questionnaire_uuid)
            "result": "Questionnaire created."
        }
        400: {
            "error": "Missing parameter.",
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
    survey = Survey.query.get_or_404(survey_uuid)

    if not owned(survey):
        return make_error(_("Lacking credentials"), 403)

    required_args = {"name", "description"}
    if questionnaire is None \
            or not all((arg in questionnaire for arg in required_args)):
        return make_error(_("Missing parameter."), 400)

    if "template" in questionnaire and questionnaire["template"] is not None:
        try:
            the_questionnaire = survey.add_new_questionnaire_from_template(
                questionnaire["name"],
                questionnaire["description"],
                questionnaire["template"]
            )
        except ObjectDoesntExistException:
            db.session.rollback()
            return make_error(_("No such template."), 404)
    else:
        the_questionnaire = Questionnaire(
            questionnaire['name'],
            questionnaire['description']
        )
        survey.questionnaires.append(the_questionnaire)

    db.session.commit()
    return jsonify({
        "result": "Questionnaire created.",
        "questionnaire": LegacyView.render(the_questionnaire)
    })


@app.route("/api/questionnaire/<int:questionnaire_uuid>", methods=["GET"])
def api_questionnaire_get(questionnaire_uuid: int):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire to retrieve.

    Response Codes:
        200: Questionnaire is returned.
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: Questionnaire {
            "class": "model.Questionnaire.Questionnaire",
            "fields": {
                "answer_count": Integer,
                "description": {
                    "class": "model.I15dString.I15dString",
                    "fields": {
                        "default_locale": language_shorthand: String,
                        "locales": {
                            language_shorthand: questionnaire_description: String
                        }
                    },
                    "uuid": String
                },
                "name": {
                    "class": "model.I15dString.I15dString",
                    "fields": {
                        "default_locale": language_shorthand: String,
                        "locales": {
                            language_shorthand: questionnaire_name: String
                        }
                    },
                    "uuid": String
                },
                "original_locale": language_shorthand: String,
                "question_count": Integer,
                "questiongroups": [QuestionGroup] (see GET
                    /api/question_group/question_group_uuid)
            },
            "uuid": String
        }
        404: {
            "error": "No such Questionnaire.",
            "result": "error"
        }
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)
    return LegacyView.jsonify(questionnaire)


@app.route("/api/questionnaire/<int:questionnaire_uuid>", methods=["PUT"])
@expect_optional(('name', str), ('description', str))
def api_questionnaire_update(
        questionnaire_uuid: int=None,
        name: str=None,
        description: str=None
):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire to update.
        name: String The new name for thie Questionnaire.
        description: String The new description for the Questionnaire.

    Sets name and description for the currently set locale.

    Response Codes:
        200: Questionnaire is successfully updated.
        403: No user is logged in or the current user doesn't have permission
            to update the given Questionnaire.
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: {
            "questionnaire": Questionnaire (see GET
                /api/questionnaire/questionnaire_uuid)
            "result": "Questionnaire updated."
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

    if name is not None:
        questionnaire.name = name
    if description is not None:
        questionnaire.description = description

    db.session.commit()
    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": LegacyView.render(questionnaire)
        })


@app.route("/api/questionnaire/<int:questionnaire_uuid>", methods=["DELETE"])
@expect(('survey_uuid', int))
def api_questionnaire_delete(questionnaire_uuid: int=None,
                             survey_uuid: int=None):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire to update.
        survey_uuid: String The uuid for the Survey on which to delete the
            Questionnaire.

    Response Codes:
        200: Questionnaire is successfully deleted.
        403: No user is logged in or the current user doesn't have permission
            to delete the given Questionnaire.
        404: The questionnaire_uuid or survey_uuid doesn't belong to a valid
            Questionnaire.

    Response Class:
        200: {
            "result": "Questionnaire deleted."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such Survey.",
            "result": "error"
        }
    """
    survey = Survey.query.get_or_404(survey_uuid)
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)
    if questionnaire not in survey.questionnaires:
        return make_error(_("Not found."), 404)

    if not owned(questionnaire):
        return make_error(_("Lacking credentials."), 403)

    survey.questionnaires.remove(questionnaire)
    db.session.commit()

    return jsonify({"result": _("Questionnaire deleted.")})


@app.route("/api/questionnaire/<int:questionnaire_uuid>/publish",
           methods=["PATCH"])
def api_questionnaire_publish(questionnaire_uuid: int):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire to update.

    Publishes the questionnaire so it is visible for outside users.

    Response Codes:
        200: Questionnaire is successfully updated.
        403: No user is logged in or the current user doesn't have permission
            to update the given Questionnaire.
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: {
            "questionnaire": Questionnaire (see GET
                /api/questionnaire/questionnaire_uuid)
            "result": "Questionnaire updated."
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
        return make_error(_("Lacking credentials."), 403)

    questionnaire.published = True
    db.session.commit()

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": LegacyView.render(questionnaire)
        })


@app.route("/api/questionnaire/<int:questionnaire_uuid>/unpublish",
           methods=["PATCH"])
def api_questionnaire_unpublish(questionnaire_uuid: int):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire to update.

    Unpublishes the questionnaire so it is not visible for outside users.

    Response Codes:
        200: Questionnaire is successfully updated.
        403: No user is logged in or the current user doesn't have permission
            to update the given Questionnaire.
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: {
            "questionnaire": Questionnaire (see GET
                /api/questionnaire/questionnaire_uuid)
            "result": "Questionnaire updated."
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
        return make_error(_("Lacking credentials."), 403)

    questionnaire.published = False
    db.session.commit()

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": LegacyView.render(questionnaire)
        })


@app.route("/api/questionnaire/<int:questionnaire_uuid>/dl/csv",
           methods=["GET"])
def api_questionnaire_download_csv(questionnaire_uuid: int):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire for which to
            generate a statistics csv.

    Response Codes:
        200: Questionnaire's statistic is returned.
        403: No user is logged in
        404: The questionnaire_uuid doesn't belong to a valid Questionnaire.

    Response Class:
        200: .csv file
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
        return make_error(_("Lacking credentials."), 403)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["question_group", "question_text", "answer_value"])

    for question_group in questionnaire.question_groups:
        for question in question_group.questions:
            for result in filter(lambda x: x.verified, question.results):
                writer.writerow(
                    [question_group.name, question.text, result.answer_value]
                )

    filename = "{}.csv".format(questionnaire_uuid)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    response.headers["Content-type"] = "text/csv"

    return response


@app.route("/api/questionnaire/templates", methods=["GET"])
def api_get_questionnaire_templates():
    """
    Parameters:
        -

    Response Codes:
        200: Questionnaire template names are returned.

    Response Class:
        200: ["template_name", ...]
    :return: 
    """
    return jsonify(list(Questionnaire.get_available_templates().keys()))
