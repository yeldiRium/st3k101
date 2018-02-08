"""
    All http endpoints that concern the rest-like api for Locale related stuff
"""

from flask import make_response
from flask.json import jsonify

from framework.internationalization.languages import Language
from main import app


@app.route("/api/locales", methods=["GET"])
def api_locales():
    return make_response(jsonify(Language.list_sorted_by_long_name()))