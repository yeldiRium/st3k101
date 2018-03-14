from flask import render_template, make_response, redirect

from main import app
from model.QuestionResult import QuestionResult
from model.Questionnaire import Questionnaire


@app.route("/verify/survey/<string:token>", methods=["GET"])
def verify_survey_submission(token:str):
    """
    An endpoint used, when email verification is enabled and the DataSubject
    follows the link sent to them via email.
    
    If the token is valid, the unverified results are verified so that they will
    be counted in the corresponding QuestionStatistic.
    
    If the token is invalid, the user is redirected to the landing page.
    
    :param token: str A random string generated on survey submission.
    :return: str HTML
    """
    unverified_results = QuestionResult.many_from_query({
        "verification_token": token,
        "verified": False
    })

    if len(unverified_results) == 0:  # nothing to verify
        return make_response(redirect("/"))

    email = None
    new_answers = dict({})

    for result in unverified_results:  # verify all results with same token
        questionnaire_uuid = result.question.questionnaire.uuid
        # check if the answer count needs to be updated on Questionnaire
        new_answers[questionnaire_uuid] = result.verify()

        # get hashed email to display it to the user
        if email is None:
            email = result.data_subject.email_hash

    # update answer count on questionnaire if needed
    for questionnaire_uuid, new_answer in new_answers.items():
        Questionnaire(questionnaire_uuid).answer_count += 1

    return render_template("survey_thanks.html", email=email)


#@app.route("/verify/users/<string:token>", methods=["GET"])
#def verify_user_account(token:str):
    # TODO: get DataClient from db by unverfied, token
    # TODO: make verified
    # TODO: redirect to backend
#    pass
