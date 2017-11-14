from flask import Flask, render_template, g, request

import auth
from framework.exceptions import ClientIpChangedException
from model.DataClient import DataClient

app = Flask(__name__)


# before and after request foo
@app.before_request
def before_request():
    """
    Called before each request, when the app context is initialized
    Automatically sets g._current_user
    """
    g._config = app.config

    session_token = request.args.get('session_token')
    g._current_user = None
    if session_token:
        if auth.activity(session_token):  # also validates token, raises ClientIpChangedException if IP pinning fails
            g._current_user = DataClient(auth.who_is(session_token))
            g._current_session_token = session_token


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Called after request is handled, before app context is deleted
    :param exception: Exception Did an exception happen?
    """
    #app.log_exception(exception)
    pass


# error handling
@app.errorhandler(ClientIpChangedException)
def client_ip_changed(error):
    """
    Called when IP pinning indicates a changed client ip between sessions
    :param error: Exception The exception object
    """
    return "LUL you're a fake and I know it"


@app.errorhandler(404)
def page_not_found(error):
    """
    Called on HTTP 404
    :param error: 
    """
    return "This is not the url you're looking for."


@app.route("/", methods=["GET"])
def home():
    """
    Home route
    """
    return render_template("home_index.html")


# SESSION STUFF:
@app.route("/register", methods=["GET"])
def register():
    """
    Registration Route
    """
    return render_template("home_register.html")


@app.route("/login", methods=["POST"])
def login():
    """
    Login Route

    Takes login parameters via POST and starts session.
    """
    return render_template("home_base.html")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout Route
    """
    return render_template("home_base.html")


# USER BACKEND
@app.route("/be/dash", methods=["GET"])
def user_dashboard():
    """
    Dashboard for users
    """
    return render_template("backend_dashboard.html")


@app.route("/be/surveys", methods=["GET"])
def user_survey_overview():
    """
    Survey overview for users
    """
    return render_template("backend_base.html")


@app.route("/be/surveys/<string:survey_uuid>", methods=["GET"])
def user_survey_details(survey_uuid):
    """
    Survey details for users
    """
    return render_template("backend_base.html")


@app.route("/be/account", methods=["GET"])
def user_account():
    """
    Account management for users
    """
    return render_template("backend_base.html")


# SURVEY FOR DATA SUBJECT
@app.route("/survey/<string:survey_uuid>", methods=["GET"])
def survey(survey_uuid):
    """
    Survey
    """
    return render_template(
        "survey_base.html",
        caption="Dis is an Example Survey",
        description="it is used to demontsrate the survey page. it has no " +
                    "content yet",
        background_color="#000000",
        font_color="#FFFFFF"
    )


@app.route("/survey/<string:survey_uuid>", methods=["POST"])
def survey_submit(survey_uuid):
    """
    Survey submit

    This endpoint receives survey data via POST and persists them. Then redi-
    rects to a thank-you page.
    """
    return ""
