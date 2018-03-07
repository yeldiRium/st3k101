"""
    All http endpoints that concern the rest-like api for DataClient
"""

from flask import g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import ObjectDoesntExistException, \
    AccessControlException
from framework.flask_request import expect_optional
from framework.internationalization import _
from framework.internationalization.languages import Language
from main import app
from model.DataClient import DataClient


@app.route("/api/account/current", methods=["GET"])
def api_account_current():
    """
    Parameters:
        None.
    TODO: update error to return 403 and Not Authorized error

    Response Codes:
        200: If a user is currently logged in, their account data is returned.
        404: If no user is logged in.

    Response class:
        200: {
            "class": "model.DataClient.DataClient",
            "fields": {
                "email": String
                "locale_name": String
            },
            "uuid": String
        }
        404: {
            "error": "Not found."
            "result": "error"
        }

    Explanation:
        locale_name is a 2/3-character shorthand for a babel language.
    """
    if not g._current_user:
        return make_error(_("Not found."), 404)
    return jsonify(g._current_user)


@app.route("/api/account/<string:account_uuid>", methods=["PUT"])
@expect_optional(('email', str), ('locale', str))
def api_account_update(account_uuid: str, email=None, locale=None):
    """
    Edits the currently logged in user's account by updating optionally email or
    locale.
    TODO: update signature, remove uuid parameter

    Parameters:
        account_uuid: String uuid for the account that should be updated.
        email: String The new email for the account.
        locale: String The new locale for the account. 2/3-character shorthand.

    Response Codes:
        200: If the account was updated accordingly. Returns the updated account
            data.
        403: If authorization failed.
        404: If the given account_uuid does not belong to an account.

    Response Class:
        200: {
            "account": DataClient (see GET /api/account/current)
            "result": "Account updated."
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
    try:
        client = DataClient(account_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    if g._current_user.uuid != account_uuid:
        return make_error(_("Lacking credentials"), 403)

    if email is not None:
        client.email = email

    if locale is not None:
        try:
            client.locale = Language[locale]
        except KeyError:
            pass

    return jsonify({
        "result": _("Account updated."),
        "account": client
    })
