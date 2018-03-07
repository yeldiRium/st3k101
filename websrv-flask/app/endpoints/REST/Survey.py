"""
    All http endpoints that concern the rest-like api for Survey
"""

from flask import g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException
from framework.internationalization import _
from main import app
from framework.flask_request import expect
from model.Survey import Survey


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
    return jsonify(g._current_user.surveys)
        # we previously listed out all surveys here.
        # This makes it, with the help of the other
        # endpoints, possible to list out all surveys
        # and all of their questions. We might need an endpoint to list
        # all surveys for admins of the platform, but
        # for this I would add a privilege check here.
        #surveys = Survey.many_from_query({})


@app.route("/api/survey", methods=["POST"])
@expect(('name', str))
def api_survey_create(name: str=''):
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

    survey = Survey.create_survey(name)
    g._current_user.surveys.add(survey)

    return jsonify({
        "result": _("Survey created."),
        "survey": survey
    })


@app.route("/api/survey/<string:survey_uuid>", methods=["GET"])
def api_survey_get(survey_uuid: str):
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
    try:
        return jsonify(Survey(survey_uuid))
    except ObjectDoesntExistException:
        return make_error(_("No such Survey."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials"), 403)


@app.route("/api/survey/<string:survey_uuid>", methods=["PUT"])
@expect(('name', str))
def api_survey_update(survey_uuid: str, name: str= ""):
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
    try:
        survey = Survey(survey_uuid)
        survey.set_name(name)
        return jsonify({
            "result": _("Survey updated."),
            "survey": survey
        })
    except ObjectDoesntExistException:
        return make_error(_("No such Survey."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)


@app.route("/api/survey/<string:survey_uuid>", methods=["DELETE"])
def api_survey_delete(survey_uuid: str= ''):
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
    try:
        survey = Survey(survey_uuid)
        g._current_user.surveys.discard(survey)
        survey.remove()
        return jsonify({"result": _("Survey deleted.")})
    except ObjectDoesntExistException:
        return make_error(_("No such Survey."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)