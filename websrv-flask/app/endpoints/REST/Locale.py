"""
    All http endpoints that concern the rest-like api for Locale related stuff
"""

from flask import make_response
from flask.json import jsonify

from main import app
from framework.internationalization import list_sorted_by_long_name


@app.route("/api/locales", methods=["GET"])
def api_locales():
    return make_response(jsonify(list_sorted_by_long_name()))