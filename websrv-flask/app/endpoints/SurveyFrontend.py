"""
    All http endpoints that are used when a DataSubject interacts with the site
"""

from flask import render_template, make_response, redirect, request, g

import utils
from framework.exceptions import ObjectDoesntExistException, \
    AccessControlException
from framework.internationalization import _
from main import app
from model.Questionnaire import Questionnaire
from model.query_access_control.QACModules import EMailVerificationQAC
from utils.email import send_mail


@app.route("/survey/<string:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid):
    """
    Endpoint for accessing questionnaires as a DataSubject.
    Serves the Questionnaire.
    :param questionnaire_uuid: str The uuid of the questionnaire in question
    :return: A response containing html
    """
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_response(redirect("/"))

    if not questionnaire.published:
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
    rects to a thank-you page. If email verification is enabled, an info
    page is displayed instead.

    In the first step errors are caught. If any is found, the survey template
    is returned again, with error messages injected.
    The field with the error must be a key on the error dict. The value is an
    optional message.
    """
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_response(redirect("/"))

    if not questionnaire.published:
        return make_response(redirect("/"))

    # check if email address was entered and all questions were answered
    error = {}
    if "email" not in request.form or request.form["email"] == "":
        error["email"] = _("Please enter an E-Mail.")
    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            if ("question_" + question.uuid) not in request.form:
                error["question_" + question.uuid] = _("Please choose a value.")

    # control all qacs and generate possibly error containing templates
    qac_templates = []
    for qac_module in questionnaire.get_qac_modules():
        qac_errors = qac_module.control()
        qac_templates.append(qac_module.render_questionnaire_template(
            qac_errors))
        if qac_errors:
            # Just set any value to true, so that the template is rendered
            error["qac"] = True

    # display errors in frontend
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

    needs_verification = False
    token = utils.generate_verification_token()
    for qac_module in questionnaire.get_qac_modules():
        if type(qac_module) is EMailVerificationQAC:
            needs_verification = True

    # update QuestionResults
    email = request.form["email"]
    answer_is_new = False
    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:

            answer_value = request.form["question_{}".format(question.uuid)]
            answer_is_new |= question.add_question_result(answer_value, email,
                                                          needs_verification,
                                                          token)

    if answer_is_new and not needs_verification:
            questionnaire.answer_count += 1

    if needs_verification:
        url = utils.generate_verification_url("/verify/survey", token)
        message = render_template(
            "mail/verification_mail.txt",
            verification_url=url,
            questionnaire_name=questionnaire.name
        )
        send_mail(email, _("Please confirm your survey submission"), message)
        return render_template("survey_please_verify.html", email=email)
    else:
        return render_template("survey_thanks.html", email=email)


@app.route("/disclaimer")
def disclaimer():
    """
    Statically serves the disclaimer page.
    :return: str HTML
    """
    return render_template("home_disclaimer.html")