from flask import Flask, render_template
from memcache import Client

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Home route
    """
    return render_template("home.html")


# SESSION STUFF:
@app.route("/register", methods=["GET"])
def register():
    """
    Registration Route
    """
    return render_template("register.html")


@app.route("/login", methods=["GET"])
def login():
    """
    Login Route
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
    return render_template("backend.html")


@app.route("/be/surveys", methods=["GET"])
def user_survey_overview():
    """
    Survey overview for users
    """
    return render_template("backend.html")


@app.route("/be/surveys/<string:survey_uuid>", methods=["GET"])
def user_survey_details(survey_uuid):
    """
    Survey details for users
    """
    return render_template("backend.html")


@app.route("/be/account", methods=["GET"])
def user_account():
    """
    Account management for users
    """
    return render_template("backend.html")


# SURVEY FOR DATA SUBJECT
@app.route("/survey/<string:survey_uuid>", methods=["GET"])
def survey(survey_uuid):
    """
    Survey
    """
    return render_template("survey.html")
