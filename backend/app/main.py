from flask import render_template, g, request, make_response, abort
from werkzeug.wrappers import Response

import auth
import auth.session
from app import app as original_app
from auth.users import PartyTypes
from framework import laziness
from framework.exceptions import *
from framework.internationalization import list_sorted_by_long_name, _
from framework.internationalization.babel_languages import babel_languages, BabelLanguage
from model.models.DataClient import DataClient
from model.models.DataSubject import DataSubject
from utils import debug_print

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

    # Setting the locale for the current request
    g._language = BabelLanguage[
        g._config["BABEL_DEFAULT_LOCALE"]
    ]  # use default locale if all fails

    # parse bearer token auth
    g._current_user = None
    g._current_session_token = None
    auth_string = request.headers.get('authorization')
    if auth_string and auth_string.startswith('Bearer'):
        try:
            session_token = auth_string.split()[1]
            if auth.session.validate_activity(session_token):
                session_record = auth.session.get_session_record(session_token)
                assert session_record['type'] in PartyTypes

                if session_record['type'] == PartyTypes.DataClient:
                    g._current_user = DataClient.query.get(auth.session.who_is(session_token))
                elif session_record['type'] == PartyTypes.DataSubject:
                    g._current_user = DataSubject.query.get(auth.session.who_is(session_token))

                if g._current_user:  # is user logged in?
                    g._current_session_token = session_token

                debug_print("Logged in as {}".format(g._current_user))
            else:
                debug_print("Session did not validate: {}".format(session_token))
                abort(401)

        except Exception as err:
            debug_print("Error during auth: {}".format(err))
            abort(401)

    # return to language handling after auth, because language may be determined
    # by user preference.
    # check HTTP accept-language
    http_locale = request.accept_languages.best_match(babel_languages.keys())
    if http_locale is not None:  # match available locales against HTTP header
        g._language = BabelLanguage[http_locale.lower()]

    # if user is logged in and a DataClient, set locale based on user prefs, override HTTP header
    if g._current_user and isinstance(g._current_user, DataClient):
        g._language = g._current_user.language

    # we also hand out a cookie the first time a locale is set and just
    if request.cookies.get('locale') is not None:
        g._language = BabelLanguage[request.cookies.get('locale').lower()]

    # Allow frontend to override locale set by browser or user.
    # This is needed to show locales to the user, even if the locale doesn't
    # match the above settings.
    requested_locale = request.args.get('locale')
    if requested_locale is not None:
        try:
            requested_locale = requested_locale.lower()
            g._language = BabelLanguage[requested_locale]
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
        job()  # TODO: remove

    # set the locale as cookie, keeps locale constant for a period of time
    if request.args.get('locale'):
        if request.args.get('locale_cookie', 1) == 1:
            response.set_cookie('locale', g._language.name)

    # we respond in the user's language
    response.headers['Content-Language'] = g._language.name
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
    return "Nisch da", 404  # render_template("home_404.html"), 404 TODO: make nice


@app.errorhandler(500)
def internal_server_error_handler(error):
    """
    Called when an uncaught exception occurs.
    We use this method to clean up any resources we might still have and exit
    cleanly.
    :param error: The exception 
    :return: Response that is sent back to the user
    """
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
        "current": g._language.value,
        "current_short": g._language.name,
        "languages": list_sorted_by_long_name()
    }
    return dict(language=language)


# Leave the following imports in place, even if your IDE tries to optimize them
# away.

# Database models
import model.models

import api.Question
import api.Session
import api.DataClient
import api.Questionnaire
import api.Dimension
import api.Language
import api.Response
import api.Tracker
import api.QuestionStatistic

# CLI commands
import cli

# signal handling
import framework.xapi.signals
