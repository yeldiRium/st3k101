from flask import render_template, make_response, redirect

from main import app
from model.QuestionResult import QuestionResult


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
    unverified_results = QuestionResult.many_from_query({"token": token,
                                                         "verified": False})
    if len(unverified_results) == 0:
        return make_response(redirect("/"))

    email = None
    for result in unverified_results:
        result.verify()
        if email is None:
            email = result.data_subject.email_hash

    return render_template("survey_thanks.html", email=email)


#@app.route("/verify/users/<string:token>", methods=["GET"])
#def verify_user_account(token:str):
    # TODO: get DataClient from db by unverfied, token
    # TODO: make verified
    # TODO: redirect to backend
#    pass
