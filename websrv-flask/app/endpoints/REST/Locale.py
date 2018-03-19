"""
    All http endpoints that concern the rest-like api for Locale related stuff
"""

from flask import make_response
from flask.json import jsonify

from main import app
from framework.internationalization import list_sorted_by_long_name

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/locales", methods=["GET"])
def api_locales():
    """
    Parameters:
        None.

    Response Codes:
        200: Returns a list of tuples of all used locales and their native name.

    Response class:
        200: [
            [
                Shorthand locale name: String,
                Native locale name: String
            ]
        ]
    """
    return make_response(jsonify(list_sorted_by_long_name()))