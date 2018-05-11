"""
    All http endpoints that are used when a DataSubject interacts with the site
"""

from flask import render_template, request

import utils
from app import app
from framework import make_error
from framework.internationalization import _
from model.SQLAlchemy import db
from utils.email import send_mail

from model.SQLAlchemy.models.QAC.QACModules.EMailVerificationQAC import \
    EMailVerificationQAC
from model.SQLAlchemy.models.Questionnaire import Questionnaire

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/survey/<int:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid: int):
    """
    Endpoint for accessing questionnaires as a DataSubject.
    Serves the Questionnaire.
    :param questionnaire_uuid: str The uuid of the questionnaire in question
    :return: A response containing html
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not questionnaire.published:
        return make_error(_("Not found."), 404)

    # generate templates for qacs without any error parameters
    qac_templates = []
    for qac_module in questionnaire.qac_modules:
        qac_templates.append(qac_module.render_questionnaire_template([]))

    return render_template(
        "survey_survey.html",
        uuid=questionnaire_uuid,
        questionnaire=questionnaire,
        qac_templates=qac_templates,
        values={},
        error={}
    )


@app.route("/survey/<int:questionnaire_uuid>", methods=["POST"])
def survey_submit(questionnaire_uuid: int):
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
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not questionnaire.published:
        return make_error(_("Not found."), 404)

    # check if email address was entered and all questions were answered
    error = {}
    if "email" not in request.form or request.form["email"] == "":
        error["email"] = _("Please enter an E-Mail.")
    for question_group in questionnaire.question_groups:
        for question in question_group.questions:
            question_str_id = "question_{}".format(question.id)
            if question_str_id not in request.form:
                error[question_str_id] = _("Please choose a value.")

    # control all qacs and generate possibly error containing templates
    qac_templates = []
    for qac_module in questionnaire.qac_modules:
        qac_errors = qac_module.control()
        qac_templates.append(qac_module.render_questionnaire_template(
            qac_errors))
        if qac_errors:
            # Just set any value to true, so that the template is rendered
            error["qac"] = True

    # display errors in frontend
    if error:
        questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)
        return render_template(
            "survey_survey.html",
            uuid=questionnaire_uuid,
            questionnaire=questionnaire,
            qac_templates=qac_templates,
            values=request.form,
            error=error
        )

    needs_verification = False
    token = utils.generate_verification_token()
    for qac_module in questionnaire.qac_modules:
        if isinstance(qac_module, EMailVerificationQAC):
            needs_verification = True

    # update QuestionResults
    email = request.form["email"]
    answer_is_new = False
    for question_group in questionnaire.question_groups:
        for question in question_group.questions:
            answer_value = request.form["question_{}".format(question.id)]
            answer_is_new |= question.add_question_result(answer_value, email,
                                                          needs_verification,
                                                          token)
    db.session.commit()

    if needs_verification:
        url = utils.generate_verification_url("/verify/survey", token)
        questionnaire_url = utils.generate_questionnaire_url(questionnaire_uuid)
        message = render_template(
            "mail/verification_mail.txt",
            verification_url=url,
            questionnaire_name=questionnaire.name,
            questionnaire_url=questionnaire_url
        )
        try:
            send_mail(email, _("Please confirm your survey submission"),
                      message)
        except Exception as e:
            error_message = "Tried to send a verification email to {}, but " \
                            "the action failed.\n\n " \
                            "Original error message:\n\n " \
                            "{}".format(email, e.args)
            app.logger.error(error_message)
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