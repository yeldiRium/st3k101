"""
    All http endpoints that concern the rest-like api for Survey
"""

from flask import g
from flask.json import jsonify

from app import app
from framework import make_error
from framework.flask_request import expect
from framework.internationalization import _
from framework.ownership import owned
from model.SQLAlchemy import db

from model.SQLAlchemy.models.Survey import Survey
from view.views.Survey import LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/survey", methods=["GET"])
def api_survey_list():
    """
    Parameters:
        None

    Lists the surveys for the currently logged in user.

    Response Codes:
        200: List of Surveys is returned.
        403: No user is logged in.

    Response Class:
        200: [Survey] (see GET /api/survey/survey_uuid)
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    return LegacyView.jsonify(g._current_user.surveys)


@app.route("/api/survey", methods=["POST"])
@expect(('name', str))
def api_survey_create(name: str=None):
    """
    Parameters:
        name: String The name for the new Survey.

    Response Codes:
        200: Survey is successfully created.
        403: No user is logged in.

    Response Class:
        200: {
            "result": "Survey created.",
            "survey": Survey
        }
        403:{
            "error": "Lacking credentials",
            "result": "error"
        }
    """
    # do not create a survey if the user is not logged in
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    survey = Survey(name=name)
    g._current_user.surveys.append(survey)
    db.session.commit()

    return jsonify({
        "result": _("Survey created."),
        "survey": LegacyView.render(survey)
    })


@app.route("/api/survey/<int:survey_uuid>", methods=["GET"])
def api_survey_get(survey_uuid: int):
    """
    Parameters:
        survey_uuid: String The uuid for the Survey to retrieve.

    Response Codes:
        200: The Survey is returned.
        403: No user is logged in or the current user doesn't have permission
            to read the given Survey.
        404: The survey_uuid doesn't belong to a valid Survey.

    Response Class:
        200: Survey {
            "class": "model.Survey.Survey",
            "fields": {
                "date_created": Date,
                "name": {
                    "class": "model.I15dString.I15dString",
                    "fields": {
                        "default_locale": language_shorthand: String,
                        "locales": {
                            language_shorthand: survey_name: String
                        }
                    },
                    "uuid": String
                },
                "original_locale": language_shorthand: String,
                "questionnaires": [Questionnaire] (see GET
                    /api/questionnaire/questionnaire_uuid)
            },
            "uuid": String
        }
        403:{
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Survey.",
            "result": "error"
        }
    """
    survey = Survey.query.get_or_404(survey_uuid)
    if not owned(survey):
        return make_error(_("Lacking credentials"), 403)
    return LegacyView.jsonify(survey)


@app.route("/api/survey/<int:survey_uuid>", methods=["PUT"])
@expect(('name', str))
def api_survey_update(survey_uuid: int, name: str= ""):
    """
    Parameters:
        survey_uuid: String The uuid for the Survey that shall be updated.
        name: String The new name for the Survey.

    Response Codes:
        200: The Survey is updated.
        403: No user is logged in or the current user doesn't have permission
            to update the given Survey.
        404: The survey_uuid doesn't belong to a valid Survey.

    Response Class:
        200: {
            "result": "Survey updated.",
            "survey": Survey (see GET /api/survey/survey_uuid)
        }
        403:{
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Survey.",
            "result": "error"
        }
    """
    survey = Survey.query.get_or_404(survey_uuid)
    if not owned(survey):
        return make_error(_("Lacking credentials"), 403)

    survey.set_name(name)
    db.session.commit()

    return jsonify({
        "result": _("Survey updated."),
        "survey": LegacyView.render(survey)
    })


@app.route("/api/survey/<int:survey_uuid>", methods=["DELETE"])
def api_survey_delete(survey_uuid: int=None):
    """
    Parameters:
        survey_uuid: String The uuid for the Survey that shall be deleted.

    Response Codes:
        200: The Survey is deleted.
        403: No user is logged in or the current user doesn't have permission
            to delete the given Survey.
        404: The survey_uuid doesn't belong to a valid Survey.

    Response Class:
        200: {
            "result": "Survey deleted."
        }
        403:{
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Survey.",
            "result": "error"
        }
    """
    survey = Survey.query.get_or_404(survey_uuid)
    if not owned(survey):
        return make_error(_("Lacking credentials"), 403)

    db.session.delete(survey)
    db.session.commit()

    return jsonify({"result": _("Survey deleted.")})
