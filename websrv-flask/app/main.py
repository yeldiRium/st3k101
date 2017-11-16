from flask import Flask, render_template, g, request
from memcache import Client
import auth
import businesslogic.users as users
from framework.exceptions import ClientIpChangedException
from model.DataClient import DataClient

from model.Questionnaire import Questionnaire
from model.QuestionGroup import QuestionGroup
from model.Question import Question

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')


# before and after request foo
@app.before_request
def before_request():
    """
    Called before each request, when the app context is initialized
    Automatically sets g._current_user
    """
    g._config = app.config

    session_token = request.args.get('session_token')
    if not session_token:
        session_token = request.cookies.get('session_token')

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
@app.route("/registration", methods=["GET"])
def registration():
    """
    Registration Route
    """
    return render_template("home_registration.html")


@app.route("/registration", methods=["POST"])
def registration_post():
    """
    Registration endpoint that takes post information for new account
    """
    data_client = users.register(request.form["email"], request.form["password"])
    return render_template(
        "home_registration_successful.html",
        data_client=data_client
    )


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
@app.route("/be/", methods=["GET"])
def backend():
    """
    Dashboard for users
    """
    return render_template("backend.html")


# SURVEY FOR DATA SUBJECT
@app.route("/survey/<string:survey_uuid>", methods=["GET"])
def survey(survey_uuid):
    """
    Survey
    """
    questionnaire = Questionnaire()
    questionnaire.name = "Teacher's thing"
    questionnaire.description = "This is an example questionnaire which is hopefully not persisted yet."

    questiongroup_1 = QuestionGroup()
    questiongroup_1.name = "Data"
    questiongroup_1.color = "#000000"
    questiongroup_1.text_color = "#FFFFFF"

    question_1_1 = Question()
    question_1_1.text = "This is a question."

    question_1_2 = Question()
    question_1_2.text = "This is not a question."

    questiongroup_1.questions += [question_1_1]
    questiongroup_1.questions += [question_1_2]

    questionnaire.questiongroups += [questiongroup_1]

    questionnaire.uuid

    return render_template(
        "survey_base.html",
        uuid=survey_uuid,
        questionnaire=questionnaire
    )


@app.route("/survey/<string:survey_uuid>", methods=["POST"])
def survey_submit(survey_uuid):
    """
    Survey submit

    This endpoint receives survey data via POST and persists them. Then redi-
    rects to a thank-you page.
    """
    return ""
