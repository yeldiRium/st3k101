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
    if not g._current_user:
        return make_error(_("Not found."), 404)

    return jsonify(g._current_user)

# FIXME: why? you should always be able to just use /api/account/current imo
#@app.route("/api/account/<string:account_uuid>", methods=["GET"])
#def api_account(account_uuid: str):
#    try:
#        return make_response(jsonify(
#            DataClient(account_uuid)
#        ))
#    except ObjectDoesntExistException:
#        return make_response(jsonify({
#            "result": "error",
#            "error": "Account doesn't exist."
#        }), 404)


@app.route("/api/account/<string:account_uuid>", methods=["PUT"])
@expect_optional(('email', str), ('locale', str))
def api_account_update(account_uuid: str, email=None, locale=None):
    try:
        client = DataClient(account_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

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
