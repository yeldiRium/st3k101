from flask import render_template

from main import app
from model.QuestionResult import QuestionResult


@app.route("/verify/survey/<string:token>", methods=["GET"])
def verify_survey_submission(token:str):
    unverified_results = QuestionResult.many_from_query({"token": token,
                                                         "verified": False})
    email = None
    for result in unverified_results:
        result.verify()
        if email is None:
            email = result.data_subject.email_hash

    return render_template("survey_thanks.html", email=email)


@app.route("/verify/users/<string:token>", methods=["GET"])
def verify_user_account(token:str):
    # TODO: get DataClient from db by unverfied, token
    # TODO: make verified
    # TODO: redirect to backend
    pass


# TODO: flask schedule job to update stats