from flask import Flask, render_template, g, request, make_response, redirect, \
    jsonify
from memcache import Client
import auth
import businesslogic.users as users
from framework.exceptions import ClientIpChangedException, \
    BadCredentialsException, UserExistsException
from model.DataClient import DataClient

from model.Survey import Survey
from model.Questionnaire import Questionnaire
from model.QuestionGroup import QuestionGroup
from model.Question import Question
from model.QuestionResult import QuestionResult
from model.DataSubject import DataSubject

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
    if not (request.form["password"] == request.form["confirmation"]):
        return render_template(
            "home_registration.html",
            reason="Password and Confirmation did not match.",
            email=request.form["email"]
        )

    try:
        data_client = users.register(request.form["email"], request.form["password"])
        return render_template(
            "home_registration_successful.html",
            data_client=data_client
        )
    except UserExistsException as e:
        return render_template(
            "home_registration.html",
            reason="User with E-Mail " + request.form["email"] + "already exists."
        )


@app.route("/login", methods=["POST"])
def login():
    """
    Login Route

    Takes login parameters via POST and starts session.
    """
    try:
        session_token = users.login(request.form["email"], request.form["password"])
        response = make_response(redirect('/be/'))
        response.set_cookie('session_token', session_token)
        return response
    except BadCredentialsException as e:
        app.log_exception(e)
        return render_template('home_index.html', login_failed=True)


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
    #if not g._current_user:
    #    return render_template('home_index.html', not_logged_in=True)
    return render_template("backend.html")


# SURVEY FOR DATA SUBJECT
@app.route("/survey/<string:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid):
    """
    Survey
    """
    survey = Survey()
    survey.name = "New Survey"

    questionnaire = Questionnaire()
    questionnaire.name = "Teacher's thing"
    questionnaire.description = "This is an example questionnaire which is hopefully not persisted yet."
    survey.questionnaires += [questionnaire]

    questiongroup_1 = QuestionGroup()
    questiongroup_1.name = "Data"
    questiongroup_1.color = "#000000"
    questiongroup_1.text_color = "#FFFFFF"

    question_1_1 = Question()
    question_1_1.text = "This is a question."
    questiongroup_1.questions += [question_1_1]

    question_1_2 = Question()
    question_1_2.text = "This is not a question."
    questiongroup_1.questions += [question_1_2]
    questionnaire.questiongroups += [questiongroup_1]

    return render_template(
        "survey_survey.html",
        uuid=questionnaire.uuid,
        questionnaire=questionnaire
    )


@app.route("/survey/<string:questionnaire_uuid>", methods=["POST"])
def survey_submit(questionnaire_uuid):
    """
    Survey submit

    This endpoint receives survey data via POST and persists them. Then redi-
    rects to a thank-you page.
    """
    data_subject = DataSubject.one_from_query({"email": request.form["email"]})
    if data_subject is None:
        data_subject = DataSubject()
        data_subject.email = request.form["email"]

    questionnaire = Questionnaire(questionnaire_uuid)

    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            current_answer = QuestionResult.one_from_query({
                "data_subject": data_subject.uuid,
                "question": question.uuid
            })
            if current_answer is None:
                current_answer = QuestionResult()
                current_answer.data_subject = data_subject
                current_answer.question = question
            current_answer.answer_value = request.form["question_" + question.uuid]

    return render_template("survey_thanks.html", email=request.form["email"])


# APIs

@app.route("/api/surveys", methods=["GET"])
def api_surveys():
    surveys = Survey.many_from_query({})
    return jsonify(surveys)
