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
    ObjectDoesntExistException, DuplicateQuestionnaireNameException
from framework.flask_request import expect, expect_optional
from framework.internationalization import _
from main import app
from model.Questionnaire import Questionnaire
from model.Survey import Survey


@app.route("/api/questionnaire/<string:questionnaire_uuid>", methods=["GET"])
def api_questionnaire_get_single(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        return jsonify(questionnaire)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found.", 404))


@app.route("/api/questionnaire/<string:questionnaire_uuid>/dl/csv",
           methods=["GET"])
def api_questionnaire_download_csv(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    # QuestionResults are not readable_by_anonymous, so the following code
    # will fail if Questionnaire was accessed anonymously
    # In other words: only the real owner may download results
    if not questionnaire.accessible():
        return make_error(_("Not found"), 404)

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


@app.route("/api/questionnaire", methods=["POST"])
@expect(('survey', str), ('questionnaire', Any))
def api_questionnaire_create(survey='', questionnaire=None):

    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    try:
        the_survey = Survey(survey)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not Found."), 404)

    required_args = {"name", "description"}
    if not all((arg in questionnaire for arg in required_args)):
        return make_error(_("Missing parameter "), 400)

    try:
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

    except DuplicateQuestionnaireNameException:
        return make_error(
            _("A Questionnaire with that name already exists"), 400)

    return jsonify({
        "result": "Questionnaire created.",
        "questionnaire": the_questionnaire
    })


@app.route("/api/questionnaire", methods=["PUT"])
@expect(('uuid', str))
@expect_optional(('name', str), ('description', str))
def api_questionnaire_update(uuid='', name=None, description=None):
    try:
        questionnaire = Questionnaire(uuid)

        # writing to readonly object will raise AccessControlException
        if name is not None:
            questionnaire.name.set_locale(name)

        if description is not None:
            questionnaire.description.set_locale(description)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    return jsonify({
            "result": _("Questionnaire updated."),
            "questionnaire": questionnaire
        })


@app.route("/api/questionnaire", methods=["DELETE"])
@expect(('uuid', str), ('survey', str))
def api_questionnaire_delete(uuid='', survey=''):
    try:
        the_survey = Survey(survey)
        questionnaire = Questionnaire(uuid)

        # might raise AccessControlException if readonly
        the_survey.remove_questionnaire(questionnaire)
        questionnaire.remove()

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    return jsonify({"result": _("Questionnaire deleted.")})
