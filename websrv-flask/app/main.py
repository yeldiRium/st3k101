import sys
import traceback

from flask import Flask, render_template, g, request, make_response, \
    jsonify, abort
from flask.ext.babel import Babel
from werkzeug.wrappers import Response

import auth
import test
from framework.exceptions import *
from framework.internationalization import list_sorted_by_long_name, _
from framework.internationalization.babel_languages import babel_languages
from framework.memcached import get_memcache
from framework.odm.DataObjectEncoder import DataObjectEncoder
from model.DataClient import DataClient


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')
app.json_encoder = DataObjectEncoder
babel = Babel(app)


# flask-babel related setup
@babel.localeselector
def get_locale():
    """
    Uses the sanest locale according to g._locale, that is set in before_request
    :return: str The locale that should be used for the current request
    by babel
    """
    return g._locale.lower()


@babel.timezoneselector
def get_timezone():
    return "Europe/Berlin"


# before and after request foo, things to do before or after each request
@app.before_request
def before_request():
    """
    Called before each request, when the app context is initialized
    Automatically sets g._current_user, g._locale
    """
    g._config = app.config

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
    g._locale = g._config["BABEL_DEFAULT_LOCALE"]  # use default locale if all fails

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
            # TODO: log error
            pass  # use previously set locale if malformed locale was requested


@app.after_request
def after_request(response: Response):

    if request.args.get('locale'):
        if request.args.get('locale_cookie', 1) == 1:
            response.set_cookie('locale', g._locale.lower())
    response.headers['Content-Language'] = g._locale.lower()
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Called after request is handled, before app context is deleted
    :param exception: Exception Did an exception happen?
    """
    pass

# error handlers for common errors, in case we didn't catch one
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
    return make_response(_("U do not kno de wae"), 404)


@app.errorhandler(500)
def internal_server_error_handler(error):
    # free all mutexes
    if hasattr(g, "_local_mutexes"):
        for mutex_uuid in g._local_mutexes:
            get_memcache().delete(mutex_uuid)
            print("Freeing {}".format(mutex_uuid), file=sys.stderr)
    else:
        print("No mutexes to free.", file=sys.stderr)
    abort(500)

@app.errorhandler(AccessControlException)
def handle_access_control_violation(error):
    print("Access Control Exception:", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    abort(404)

@app.context_processor
def inject_languages():
    """
    Inject languages parameters into all templates.
    """
    language = {
        "current": g._locale,
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
        return render_template('home_index.html', not_logged_in=True)
    return render_template("backend.html")

# Survey Frontend, what DataSubject sees
import endpoints.SurveyFrontend

# Auth related pages like login, registration
import endpoints.Auth

# APIs
import endpoints.REST.Survey
import endpoints.REST.Questionnaire
import endpoints.REST.QuestionGroup
import endpoints.REST.Question
import endpoints.REST.QAC
import endpoints.REST.Account
import endpoints.REST.Locale

@app.route("/test/runall", methods=["POST"])
def api_test_runall():
    # FIXME: remove (WHOLE METHOD) in production
    # if g._current_user is None:
    #    return abort(403)

    return make_response(jsonify({
        "result": test.run_all()
    }))
