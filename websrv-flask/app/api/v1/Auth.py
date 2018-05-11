"""
    All http endpoints that concern auth and user session, like logging in & out
"""

from flask import render_template, request, make_response, redirect

from auth import users
from framework.exceptions import UserExistsException, BadCredentialsException, \
    UserNotLoggedInException
from app import app
from framework.internationalization import _
from model.SQLAlchemy import db

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/registration", methods=["GET"])
def registration():
    """
    Registration Route
    """
    return render_template("home_registration.html")


@app.route("/registration", methods=["POST"])
def registration_post():
    """
    Registration endpoint that takes post information for new account
    """
    # TODO: make users start out as unverified
    if request.form["password"] != request.form["confirmation"]:
        return render_template(
            "home_registration.html",
            reason=_("Password and Confirmation did not match."),
            email=request.form["email"]
        )

    try:
        data_client = users.register(request.form["email"],
                                     request.form["password"])
        db.session.commit()
        return render_template(
            "home_registration_successful.html",
            data_client=data_client
        )
    except UserExistsException as e:
        db.session.rollback()
        return render_template(
            "home_registration.html",
            reason=e.args[0]
        )


@app.route("/login", methods=["POST"])
def login():
    """
    Login Route

    Takes login parameters via POST and starts session.
    """
    # TODO: disallow login for unverified users
    try:
        session_token = users.login(request.form["email"],
                                    request.form["password"])
        response = make_response(redirect('/be/'))
        response.set_cookie('session_token', session_token)
        return response
    except BadCredentialsException:
        app.logger.info(
            "Invalid login attempt: {}".format(request.form["email"]))
        return render_template('home_index.html', login_failed=True)


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout Route
    """
    try:
        users.logout()
    except UserNotLoggedInException:
        pass
    finally:
        return make_response(redirect('/'))
