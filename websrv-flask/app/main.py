from flask import Flask, render_template, g, request, make_response, redirect, \
    jsonify

import auth
import businesslogic.users as users
from framework.exceptions import *
from framework.odm.PersistentObjectEncoder import PersistentObjectEncoder
from model.DataClient import DataClient
from model.DataSubject import DataSubject
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.QuestionResult import QuestionResult
from model.Questionnaire import Questionnaire
from model.Survey import Survey

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')
app.json_encoder = PersistentObjectEncoder


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
    return make_response("This is not the url you're looking for.", 404)


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
    if not g._current_user:
        return render_template('home_index.html', not_logged_in=True)
    return render_template("backend.html")


# SURVEY FOR DATA SUBJECT
@app.route("/survey_test", methods=["GET"])
def survey_test():
    """
    test Survey, always generates a new questionnaire
    """
    survey = Survey()
    survey.name = "New Test Survey"
    questionnaire = survey.add_new_questionnaire(
        "Teacher's thingy 2",
        "This is an example questionnaire which is hopefully not persisted yet."
    )

    questiongroup_1 = QuestionGroup()
    questiongroup_1.name = "Data"
    questiongroup_1.color = "#000000"
    questiongroup_1.text_color = "#FFFFFF"
    questionnaire.questiongroups.add(questiongroup_1)

    questionnaire.add_question_to_group(questiongroup_1, "This is a question.")
    questionnaire.add_question_to_group(questiongroup_1, "This is not a question.")

    return render_template(
        "survey_survey.html",
        uuid=questionnaire.uuid,
        questionnaire=questionnaire
    )


@app.route("/survey/<string:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        return render_template(
            "survey_survey.html",
            uuid=questionnaire_uuid,
            questionnaire=questionnaire
        )
    except ObjectDoesntExistException as _:
        return make_response(redirect("/"))


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

    questionnaire.answer_count += 1

    return render_template("survey_thanks.html", email=request.form["email"])


# APIs

@app.route("/api/survey", methods=["GET"])
def api_survey_list():
    surveys = Survey.many_from_query({})
    return jsonify(surveys)


@app.route("/api/survey", methods=["Post"])
def api_survey_create():
    data = request.get_json()
    survey = Survey()
    survey.name = data["name"]

    return jsonify({
        "result": "Survey created.",
        "survey": survey
    })


@app.route("/api/survey", methods=["PUT"])
def api_survey_update():
    data = request.get_json()
    try:
        survey = Survey(data["uuid"])
        survey.name = data["name"]
        return jsonify({
            "result": "Survey updated.",
            "survey": survey
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Survey doesn't exist."
        }, 400)


@app.route("/api/survey", methods=["DELETE"])
def api_survey_delete():
    data = request.get_json()
    try:
        survey = Survey(data["uuid"])
        # TODO: delete subobjects
        survey.remove()
        return jsonify({
            "result": "Survey deleted."
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Survey doesn't exist."
        }, 400)


@app.route("/api/questionnaire/<string:questionnaire_uuid>", methods=["GET"])
def api_questionnaire_get_single(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        return jsonify(questionnaire)
    except ObjectDoesntExistException as e:
        return make_response(jsonify({
            "result": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/questionnaire", methods=["POST"])
def api_questionnaire_create():
    data = request.get_json()
    survey = Survey(data["survey"])
    try:
        if "template" in data["questionnaire"]:
            if data["questionnaire"]["template"] == "efla_teacher":
                questionnaire = survey.add_new_questionnaire_from_efla_teacher(
                    data["questionnaire"]["name"],
                    data["questionnaire"]["description"]
                )
            elif data["questionnaire"]["template"] == "efla_student":
                questionnaire = survey.add_new_questionnaire_from_efla_student(
                    data["questionnaire"]["name"],
                    data["questionnaire"]["description"]
                )
            else:
                questionnaire = survey.add_new_questionnaire_from_template(
                    data["questionnaire"]["name"],
                    data["questionnaire"]["description"],
                    Questionnaire(data["questionnaire"]["template"])
                )
        else:
            questionnaire = survey.add_new_questionnaire(
                data["questionnaire"]["name"],
                data["questionnaire"]["description"]
            )
        return jsonify({
            "result": "Questionnaire created.",
            "questionnaire": questionnaire
        })
    except DuplicateQuestionnaireNameException as e:
        return jsonify({
            "error": "Questionnaire with name \"" + data["questionnaire"]["name"] + "\" already exists."
        }, 400)


@app.route("/api/questionnaire", methods=["PUT"])
def api_questionnaire_update():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["uuid"])
        if "name" in data:
            questionnaire.name = data["name"]
        if "description" in data:
            questionnaire.description = data["description"]
        return jsonify({
            "result": "Questionnaire updated.",
            "questionnaire": questionnaire
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Questionnaire doesn't exist."
        }, 400)


@app.route("/api/questionnaire", methods=["DELETE"])
def api_questionnaire_delete():
    data = request.get_json()
    try:
        survey = Survey(data["survey"])
        questionnaire = Questionnaire(data["uuid"])
        survey.remove_questionnaire(questionnaire)
        return jsonify({
            "result": "Questionnaire deleted."
        })
    except ObjectDoesntExistException as e:
        return make_response(jsonify({
            "result": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/question_group", methods=["POST"])
def api_questiongroup_create():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["questionnaire"])
        question_group = QuestionGroup()
        question_group.name = data["name"]
        question_group.color = "#000000"
        question_group.text_color = "#FFFFFF"
        questionnaire.questiongroups.add(question_group)
        return jsonify({
            "result": "QuestionGroup created.",
            "question_group": question_group
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Questionnaire doesn't exist."
        }, 400)


@app.route("/api/question_group", methods=["PUT"])
def api_questiongroup_update():
    data = request.get_json()
    try:
        question_group = QuestionGroup(data["uuid"])
        if "name" in data:
            question_group.name = data["name"]
        if "color" in data:
            question_group.color = data["color"]
        if "text_color" in data:
            question_group.text_color = data["text_color"]
        return jsonify({
            "result": "QuestionGroup updated.",
            "question_group": question_group
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "QuestionGroup doesn't exist."
        }, 400)


@app.route("/api/question_group", methods=["DELETE"])
def api_questiongroup_delete():
    data = request.get_json()
    try:
        question_group = QuestionGroup(data["uuid"])
        questionnaire = Questionnaire(data["questionnaire"])
        questionnaire.questiongroups.remove(question_group)
        # TODO: delete subobjects. MEMORY LEAK
        question_group.remove()
        return jsonify({
            "result": "QuestionGroup deleted."
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "QuestionGroup doesn't exist."
        }, 400)


@app.route("/api/question", methods=["POST"])
def api_question_create():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["questionnaire"])
        question_group = QuestionGroup(data["question_group"])
        question = questionnaire.add_question_to_group(question_group, data["text"])
        return jsonify({
            "result": "Question created.",
            "question": question
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "QuestionGroup doesn't exist."
        }, 400)


@app.route("/api/question", methods=["PUT"])
def api_question_update():
    data = request.get_json()
    try:
        question = Question(data["uuid"])
        question.text = data["text"]
        return jsonify({
            "result": "Question updated.",
            "question": Question
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Question doesn't exist."
        }, 400)


@app.route("/api/question", methods=["DELETE"])
def api_question_delete():
    data = request.get_json()
    try:
        question = Question(data["uuid"])
        question_group = QuestionGroup(data["question_group"])
        questionnaire = Questionnaire(data["questionnaire"])
        questionnaire.remove_question_from_group(question_group, question)
        # TODO: remove all answers to deleted question
        return jsonify({
            "result": "Question deleted."
        })
    except ObjectDoesntExistException as e:
        return jsonify({
            "result": "Question doesn't exist."
        }, 400)
