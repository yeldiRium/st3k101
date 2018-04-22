import sys

from flask import render_template, g, request, make_response, abort
from werkzeug.wrappers import Response

import auth
from app import app as original_app
from framework import laziness
from framework.exceptions import *
from framework.internationalization import list_sorted_by_long_name, _
from framework.internationalization.babel_languages import babel_languages
from framework.memcached import get_memcache
from model.ODM.DataClient import DataClient

__author__ = "Noah Hummel, Hannes Leutloff"


app = original_app


# Things that happen on each request
@app.before_request
def before_request():
    """
    Called before each request, when the app context is initialized
    Automatically sets g._current_user, g._locale
    """
    g._config = app.config  # g is always reachable, app might not be

    # Try to detect session based on session token
    session_token = request.args.get('session_token')
    if not session_token:
        session_token = request.cookies.get('session_token')

    g._current_user = None
    if session_token:
        # also validates token, raises ClientIpChangedException if
        # IP pinning fails
        if auth.validate_activity(session_token):
            g._current_user = DataClient(auth.who_is(session_token))
            g._current_session_token = session_token

    # Setting the locale for the current request
    g._locale = g._config[
        "BABEL_DEFAULT_LOCALE"]  # use default locale if all fails

    # check HTTP accept-language
    http_locale = request.accept_languages.best_match(babel_languages.keys())
    if http_locale is not None:  # match available locales against HTTP header
        g._locale = http_locale.lower()

    # if user is logged in, set locale based on user prefs, override HTTP header
    if g._current_user:
        g._locale = g._current_user.locale

    # we also hand out a cookie the first time a locale is set and just
    if request.cookies.get('locale'):
        g._locale = request.cookies.get('locale').lower()

    # Allow frontend to override locale set by browser or user.
    # This is needed to show locales to the user, even if the locale doesn't
    # match the above settings. Otherwise, a german user wouldn't be able to see
    # a french survey, even if they spoke french. The frontend may prompt the
    # user if they want to see a locale that they mightn't understand.
    requested_locale = request.args.get('locale')
    if requested_locale is not None:
        try:
            requested_locale = requested_locale.lower()
            g._locale = requested_locale
        except (AttributeError, KeyError):
            pass  # use previously set locale if malformed locale was requested


@app.after_request
def after_request(response: Response):
    """
    Called before response is sent to client.
    We may transform the response before sending it out.
    :param response: Reponse That is about to be sent back
    :return: Response the response that is sent back to the client
    """
    # hacky scheduling
    for job in laziness.LAZY_JOBS:
        job()

    # set the locale as cookie, keeps locale constant for a period of time
    if request.args.get('locale'):
        if request.args.get('locale_cookie', 1) == 1:
            response.set_cookie('locale', g._locale.lower())

    # we respond in the user's language
    response.headers['Content-Language'] = g._locale.lower()
    return response


# Error handlers
@app.errorhandler(ClientIpChangedException)
def client_ip_changed(error):
    """
    Called when IP pinning indicates a changed client ip between sessions
    :param error: Exception The exception object
    """
    return make_response(_("U been doin bad stuff"), 403)


@app.errorhandler(404)
def page_not_found(error):
    """
    Called on HTTP 404
    :param error: L'Error
    """
    return render_template("home_404.html"), 404


@app.errorhandler(500)
def internal_server_error_handler(error):
    """
    Called when an uncaught exception occurs.
    We use this method to clean up any resources we might still have and exit
    cleanly.
    :param error: The exception 
    :return: Response that is sent back to the user
    """
    # free all mutexes in memcache so that we don't lock up any DataObjects
    if hasattr(g, "_local_mutexes"):
        for mutex_uuid in g._local_mutexes:
            get_memcache().delete(mutex_uuid)
            print("Freeing {}".format(mutex_uuid), file=sys.stderr)
    else:
        print("No mutexes to free.", file=sys.stderr)
    return make_response(error, 500)  # TODO: nice error page


@app.errorhandler(AccessControlException)
def handle_access_control_violation(error):
    """
    Called when an uncaught AccessControlException occurs.
    We pretend we don't know the resource in question and respond with 404.
    :param error: The error.
    :return: None
    """
    abort(404)


@app.context_processor
def inject_languages():
    """
    Injects languages parameters into all jinja templates.
    """
    language = {
        "current": babel_languages[g._locale],
        "current_short": g._locale,
        "languages": list_sorted_by_long_name()
    }
    return dict(language=language)


# Landing Page
@app.route("/", methods=["GET"])
def home():
    """
    Home route
    """
    return render_template("home_index.html")


# Dashboard / Backend for DataClients
@app.route("/be/", methods=["GET"])
def backend():
    """
    Dashboard for users
    """
    if not g._current_user:
        return render_template("home_index.html", not_logged_in=True)
    return render_template("backend.html")


# Leave the following imports in place, even if your IDE tries to optimize them
# away.

# Database models
import model.SQLAlchemy.models

# Survey Frontend, what DataSubject sees
import api.v1.SurveyFrontend
import api.v1.Verification

# Auth related pages like login, registration
import api.v1.Auth

# APIs
import api.v1.REST.Survey
import api.v1.REST.Questionnaire
import api.v1.REST.QuestionGroup
import api.v1.REST.Question
import api.v1.REST.QAC
import api.v1.REST.Account
import api.v1.REST.Locale
import api.v1.REST.Statistic

# CLI commands
import cli
