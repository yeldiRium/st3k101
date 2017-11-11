from flask import Flask, render_template, g

app = Flask(__name__)
g._config = app.config


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
