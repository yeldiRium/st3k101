"""
    All http endpoints that are used when a DataSubject interacts with the site
"""

from flask import render_template, make_response, redirect, request

from framework.exceptions import ObjectDoesntExistException, \
    AccessControlException
from framework.internationalization import _
from main import app
from model.DataClient import DataClient
from model.DataSubject import DataSubject
from model.QuestionResult import QuestionResult
from model.Questionnaire import Questionnaire


@app.route("/survey/<string:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_response(redirect("/"))

    # generate templates for qacs without any error parameters
    qac_templates = []
    for qac_module in questionnaire.get_qac_modules():
        qac_templates.append(qac_module.render_questionnaire_template([]))

    return render_template(
        "survey_survey.html",
        uuid=questionnaire_uuid,
        questionnaire=questionnaire,
        qac_templates=qac_templates,
        values={},
        error={}
    )


@app.route("/survey/<string:questionnaire_uuid>", methods=["POST"])
def survey_submit(questionnaire_uuid):
    """
    Survey submit

    This endpoint receives survey data via POST and persists them. Then redi-
    rects to a thank-you page.

    In the first step errors are caught. If any is found, the survey template
    is returned again, with error messages injected.
    The field with the error must be a key on the error dict. The value is an
    optional message.
    """
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_response(redirect("/"))

    error = {}
    if "email" not in request.form or request.form["email"] == "":
        error["email"] = _("Please enter an E-Mail.")
        # TODO: check if email is valid
    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            if ("question_" + question.uuid) not in request.form:
                error["question_" + question.uuid] = _("Please choose a value.")

    # control all qacs and generate possibly error containing templates
    qac_templates = []
    for qac_module in questionnaire.get_qac_modules():
        qac_errors = qac_module.control()
        qac_templates.append(qac_module.render_questionnaire_template(qac_errors))
        if qac_errors:
            # Just set any value to true, so that the template is rendered
            error["qac"] = True

    if error:
        try:
            questionnaire = Questionnaire(questionnaire_uuid)
            return render_template(
                "survey_survey.html",
                uuid=questionnaire_uuid,
                questionnaire=questionnaire,
                qac_templates=qac_templates,
                values=request.form,
                error=error
            )
        except (AccessControlException, ObjectDoesntExistException):
            return make_response(redirect("/"))

    data_subject = DataSubject.one_from_query(
        {"email_hash": request.form["email"]})
    if data_subject is None:
        data_subject = DataSubject()
        data_subject.email = request.form["email"]

    answer_overwritten = False
    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            current_answer = QuestionResult.one_from_query({
                "data_subject": data_subject.uuid,
                "question": question.uuid
            })
            if current_answer is None:
                current_answer = QuestionResult(
                    owner=DataClient(question.owner_uuid))
                current_answer.data_subject = data_subject
                current_answer.question = question
                question.add_question_result(current_answer)
            else:
                answer_overwritten = True
            current_answer.answer_value = request.form[
                "question_" + question.uuid]
            question.statistic.update()
    if not answer_overwritten:
        questionnaire.answer_count += 1

    return render_template("survey_thanks.html", email=request.form["email"])


@app.route(
    "/survey/<string:questionnaire_uuid>/confirm/<string:confirmation_token>")
def survey_confirm_submission(questionnaire_uuid, confirmation_token):
    pass


@app.route("/disclaimer")
def disclaimer():
    return render_template("home_disclaimer.html")