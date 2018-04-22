"""
    All http endpoints that concern authentication logic.
"""

from flask import g
from flask.json import jsonify

from auth import users
from framework.exceptions import BadCredentialsException, \
    UserNotLoggedInException
from framework.flask_request import expect
from main import app

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/auth/login", methods=["POST"])
@expect(
    ("email", str),
    ("password", str)
)
def apilogin(email: str, password: str):
    """
    Parameters:
        email: String The email for the user to be logged in.
        password: Object The matching password.

    Response Codes:
        200: User logged in successfully.
        403: Bad credentials; User not logged in.

    Response Class:
        200: {
            "session_token": string
        }
        403: {
            "error": "Bad credentials.",
            "result": "error"
        }
    """
    try:
        session_token = users.login(email, password)
        response = jsonify({"session_token": session_token})
        response.set_cookie('session_token', session_token)
        return response
    except BadCredentialsException:
        app.logger.info("Invalid login attempt: {}".format(email))
        return jsonify({
            "result": "error",
            "reason": "Bad credentials."
        }, 403)


@app.route("/api/auth/logout", methods=["GET"])
def apilogout():
    """
    Idempotent. Will always return successful logout message, even if not logged
    in.

    Response Codes:
        200: User logged out successfully.

    Response Class:
        200: {
            "result": "User logged out."
        }
    """
    try:
        users.logout()
    except UserNotLoggedInException:
        pass
    finally:
        return jsonify({
            "result": "User logged out."
        })


@app.route("/api/auth/<string:session_token>/isValid", methods=["GET"])
def api_is_session_valid(session_token: str):
    """
    Checks, if a session token is valid for the current session.

    Response Codes:
        200: Session token checked.

    Response Class:
        200: {
            "result": True/False
        }
    """
    if session_token is g._current_session_token:
        return jsonify({
            "result": True
        })
    else:
        return jsonify({
            "result": False
        })
