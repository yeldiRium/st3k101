from flask import Flask, render_template
from memcache import Client

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    """
    Home route
    """
    return render_template("base.html")


# SESSION STUFF:
@app.route("/register", methods=["GET"])
def register():
    """
    Registration Route
    """
    return ""


@app.route("/login", methods=["GET"])
def login():
    """
    Login Route
    """
    return ""


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout Route
    """
    return ""


# USER BACKEND
@app.route("/be/dash", methods=["GET"])
def user_dashboard():
    """
    Dashboard for users
    """
    return ""


@app.route("/be/surveys", methods=["GET"])
def user_survey_overview():
    """
    Survey overview for users
    """
    return ""


@app.route("/be/surveys/<string:survey_uuid>", methods=["GET"])
def user_survey_details(survey_uuid):
    """
    Survey details for users
    """
    return ""


@app.route("/be/account", methods=["GET"])
def user_account():
    """
    Account management for users
    """
    return ""


# SURVEY FOR DATA SUBJECT
@app.route("/survey/<string:survey_uuid", methods=["GET"])
def survey(survey_uuid):
    """
    Survey
    """
    return ""
