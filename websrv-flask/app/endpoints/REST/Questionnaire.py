"""
    All http endpoints that concern the rest-like api for Questionnaire
    
    Note that some endpoints for QAC also start with '/api/questionnaire'.
    These endpoints can be found in QAC.py
"""
import csv
import io
from typing import Any

from flask import make_response, g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from main import app
from model.Questionnaire import Questionnaire
from model.Survey import Survey


@app.route("/api/questionnaire", methods=["POST"])
@expect(
    ('survey_uuid', str),
    ('questionnaire', Any)
)
def api_questionnaire_create(survey_uuid: str=None, questionnaire: Any=None):
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
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    try:
        the_survey = Survey(survey_uuid)
    except ObjectDoesntExistException:
        return make_error(_("No such Survey."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not the_survey.accessible():
        return make_error(_("Lacking credentials"), 403)

    required_args = {"name", "description"}
    if questionnaire is None \
            or not all((arg in questionnaire for arg in required_args)):
        return make_error(_("Missing parameter."), 400)

    if "template" in questionnaire:
        the_questionnaire = the_survey.add_new_questionnaire_from_template(
            questionnaire["name"],
            questionnaire["description"],
            questionnaire["template"]
        )
    else:
        the_questionnaire = the_survey.add_new_questionnaire(
            questionnaire["name"],
            questionnaire["description"]
        )

    return jsonify({
        "result": "Questionnaire created.",
        "questionnaire": the_questionnaire
    })


@app.route("/api/questionnaire/<string:questionnaire_uuid>", methods=["GET"])
def api_questionnaire_get(questionnaire_uuid: str):
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
    try:
        return jsonify(Questionnaire(questionnaire_uuid))
    except ObjectDoesntExistException:
        return make_error(_("Not found."), 404)


@app.route("/api/questionnaire/<questionnaire_uuid>", methods=["PUT"])
@expect_optional(('name', str), ('description', str))
def api_questionnaire_update(
        questionnaire_uuid: str= '',
        name: str= '',
        description: str= ''
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
    try:
        questionnaire = Questionnaire(questionnaire_uuid)

        if name is not None:
            questionnaire.set_name(name)
        if description is not None:
            questionnaire.set_description(description)
    except ObjectDoesntExistException:
        return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    if not questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": questionnaire
        })


@app.route("/api/questionnaire/<string:questionnaire_uuid>", methods=["DELETE"])
@expect(('survey_uuid', str))
def api_questionnaire_delete(questionnaire_uuid: str=None, survey_uuid: str=None):
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
    try:
        the_survey = Survey(survey_uuid)
        questionnaire = Questionnaire(questionnaire_uuid)

        # might raise AccessControlException if readonly
        the_survey.remove_questionnaire(questionnaire)
    except ObjectDoesntExistException as e:
        if e.args[1] == "Questionnaire":
            return make_error(_("No such Questionnaire."), 404)
        else:
            return make_error(_("No such Survey."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    return jsonify({"result": _("Questionnaire deleted.")})


@app.route("/api/questionnaire/<string:questionnaire_uuid>/publish",
           methods=["PATCH"])
def api_questionnaire_publish(questionnaire_uuid: str):
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
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        questionnaire.published = True
    except ObjectDoesntExistException:
        return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": questionnaire
        })

@app.route("/api/questionnaire/<string:questionnaire_uuid>/unpublish",
           methods=["PATCH"])
def api_questionnaire_unpublish(questionnaire_uuid: str):
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
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        questionnaire.published = False
    except ObjectDoesntExistException:
        return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": questionnaire
        })


@app.route("/api/questionnaire/<string:questionnaire_uuid>/dl/csv",
           methods=["GET"])
def api_questionnaire_download_csv(questionnaire_uuid: str):
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
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except ObjectDoesntExistException:
        return make_error(_("No such Questionnaire."), 404)
    except AccessControlException:
        return make_error(_("Lacking credentials."), 403)

    # QuestionResults are not readable_by_anonymous, so the following code
    # will fail if Questionnaire was accessed anonymously
    # In other words: only the real owner may download results
    if not questionnaire.accessible():
        return make_error(_("Lacking credentials."), 403)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["question_group", "question_text", "answer_value"])

    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            for result in filter(lambda x: x.verified, question.results):
                writer.writerow([question_group.name.get_default_text(),
                                 question.text.get_default_text(),
                                 result.answer_value])

    filename = "{}.csv".format(questionnaire_uuid)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    response.headers["Content-type"] = "text/csv"

    return response
