"""
    All http endpoints that concern the rest-like api for DataClient
"""

from flask import g
from flask.json import jsonify

from app import app
from framework import make_error
from framework.flask_request import expect_optional
from framework.internationalization import _, babel_languages
from model.SQLAlchemy import db

from model.SQLAlchemy.models.DataClient import DataClient
from view.views.DataClient import LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/account/current", methods=["GET"])
def api_account_current():
    """
    Parameters:
        None.

    Response Codes:
        200: If a user is currently logged in, their account data is returned.
        403: If no user is logged in.

    Response class:
        200: {
            "class": "model.DataClient.DataClient",
            "fields": {
                "email": String
                "locale_name": String
            },
            "uuid": String
        }
        403: {
            "error": "Lacking credentials."
            "result": "error"
        }

    Explanation:
        locale_name is a 2/3-character shorthand for a babel language.
    """
    if not g._current_user:
        return make_error(_("Lacking credentials."), 403)
    return LegacyView.jsonify(g._current_user)


@app.route("/api/account/current", methods=["PUT"])
@expect_optional(('email', str), ('locale', str))
def api_account_update(email: str=None, locale: str=None):
    """
    Edits the currently logged in user's account by updating optionally email or
    locale.

    Parameters:
        email: String The new email for the account.
        locale: String The new locale for the account. 2/3-character shorthand.

    Response Codes:
        200: If the account was updated accordingly. Returns the updated account
            data.
        400: If the given locale is not a valid shorthand.
        403: If authorization failed.
        404: If the given account_uuid does not belong to an account.

    Response Class:
        200: {
            "account": DataClient (see GET /api/account/current)
            "result": "Account updated."
        }
        400: {
            "error": "Invalid locale.",
            "result": "error
        }
        400: {
            "error": "That email address is already in use.",
            "result": error"
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "Not found.",
            "result": "error"
        }

    Explanation:
        locale_name is a 2/3-character shorthand for a babel language.
    """
    if not g._current_user:
        return make_error(_("Lacking credentials."), 403)

    if email is not None:
        user_with_email = DataClient.query.filter_by(email=email).first()
        if user_with_email is not None:
            return make_error(_("That email address is already in use."), 400)
        g._current_user.email = email

    if locale is not None:
        if locale not in babel_languages:
            return make_error(_("Invalid locale."), 400)
        g._current_user.locale = locale

    db.session.commit()

    return jsonify({
        "result": _("Account updated."),
        "account": LegacyView.render(g._current_user)
    })