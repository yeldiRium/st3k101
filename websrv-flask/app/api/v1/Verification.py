from flask import render_template, make_response, redirect
from app import app
from model.SQLAlchemy import db

from model.SQLAlchemy.models.QuestionResult import QuestionResult

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/verify/survey/<string:token>", methods=["GET"])
def verify_survey_submission(token: str):
    """
    An endpoint used, when email verification is enabled and the DataSubject
    follows the link sent to them via email.
    
    If the token is valid, the unverified results are verified so that they will
    be counted in the corresponding QuestionStatistic.
    
    If the token is invalid, the user is redirected to the landing page.
    
    :param token: str A random string generated on survey submission.
    :return: str HTML
    """
    unverified_results = QuestionResult.query.filter_by(
        verification_token=token,
        verified=False
        ).all()

    if len(unverified_results) == 0:  # nothing to verify
        return make_response(redirect("/"))

    email = None
    for result in unverified_results:  # verify all results with same token
        result.verify()

        # get email to display it to the user
        if email is None:
            email = result.data_subject.email

    db.session.commit()
    return render_template("survey_thanks.html", email=email)


# @app.route("/verify/users/<string:token>", methods=["GET"])
# def verify_user_account(token:str):
    # TODO: get DataClient from db by unverfied, token
    # TODO: make verified
    # TODO: redirect to backend
#    pass
