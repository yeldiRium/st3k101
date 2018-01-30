import sys
from flask import Flask, render_template, g, request, make_response, redirect, \
    jsonify, abort
from werkzeug.wrappers import Response

import auth
import businesslogic.users as users
import test
import io
import csv
from businesslogic.QACFactory import create_qac_module
from framework.exceptions import *
from framework.internationalization.languages import Language
from framework.odm.DataObjectEncoder import DataObjectEncoder
from model.DataClient import DataClient
from model.DataSubject import DataSubject
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.QuestionResult import QuestionResult
from model.Questionnaire import Questionnaire
from model.Survey import Survey

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_PATH')
app.json_encoder = DataObjectEncoder


# before and after request foo
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
        if auth.activity(
                session_token):  # also validates token, raises ClientIpChangedException if IP pinning fails
            g._current_user = DataClient(auth.who_is(session_token))
            g._current_session_token = session_token

    # Setting the locale for the current request
    g._locale = g._config["DEFAULT_LOCALE"]  # use default locale if all else fails

    http_locale = request.accept_languages.best_match((l.name.lower() for l in Language))  # check HTTP accept-language
    if http_locale is not None:  # try to match available locales against HTTP header
        g._locale = Language[http_locale.upper()]

    if g._current_user:  # if user is logged in, set locale based on user preferences, override HTTP header
        g._locale = g._current_user.locale

    if request.cookies.get('locale'):
        g._locale = Language[request.cookies.get('locale')]

    # Allow frontend to override locale set by browser or user. This is needed to show locales to the user, even if the
    # locale doesn't match the above settings. Otherwise, a german user wouldn't be able to see a french survey, even if
    # they spoke french. The frontend may prompt the user if they want to see a locale that they mightn't understand.
    requested_locale = request.args.get('locale')
    if requested_locale is not None:
        try:
            requested_locale = Language[requested_locale]
            g._locale = requested_locale
        except (AttributeError, KeyError):
            # TODO: log error
            pass  # use previously set locale if malformed locale was requested

@app.after_request
def after_request(response: Response):
    if request.args.get('locale'):
        response.set_cookie('locale', g._locale.name)
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Called after request is handled, before app context is deleted
    :param exception: Exception Did an exception happen?
    """
    # app.log_exception(exception)
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
    :param error: L'Error
    """
    return make_response("This is not the url you're looking for.", 404)

@app.errorhandler(500)
def internal_server_error_handler(error):
    # free all mutexes
    for o in g._persistent_objects.values():
        o.__del__()  # FIXME: dis ain't avoiding deadlocks at all

@app.errorhandler(AccessControlException)
def handle_access_control_violation(error):
    abort(404)


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
        data_client = users.register(request.form["email"],
                                     request.form["password"])
        return render_template(
            "home_registration_successful.html",
            data_client=data_client
        )
    except UserExistsException as e:
        return render_template(
            "home_registration.html",
            reason="User with E-Mail " + request.form[
                "email"] + "already exists."
        )


@app.route("/login", methods=["POST"])
def login():
    """
    Login Route

    Takes login parameters via POST and starts session.
    """
    try:
        session_token = users.login(request.form["email"],
                                    request.form["password"])
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
    users.logout()
    return make_response(redirect('/'))


# USER BACKEND
@app.route("/be/", methods=["GET"])
def backend():
    """
    Dashboard for users
    """
    if not g._current_user:
        return render_template('home_index.html', not_logged_in=True)
    return render_template("backend.html")


# SURVEY FOR DATA SUBJECT FIXME: remove
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
    questionnaire.add_question_to_group(questiongroup_1,
                                        "This is not a question.")

    return render_template(
        "survey_survey.html",
        uuid=questionnaire.uuid,
        questionnaire=questionnaire
    )


@app.route("/survey/<string:questionnaire_uuid>", methods=["GET"])
def survey(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)

        # generate templates for qacs without any error parameters
        qac_templates = []
        for qac_module in questionnaire.get_qac_modules():
            qac_templates.append(qac_module.get_survey_template({}))

        return render_template(
            "survey_survey.html",
            uuid=questionnaire_uuid,
            questionnaire=questionnaire,
            qac_templates=[],
            values={},
            error={}
        )
    except ObjectDoesntExistException as _:
        return make_response(redirect("/"))


@app.route("/survey/<string:questionnaire_uuid>", methods=["POST"])
def survey_submit(questionnaire_uuid):
    """
    Survey submit

    This endpoint receives survey data via POST and persists them. Then redi-
    rects to a thank-you page.

    In the first step errors are caught. If any is found, the survey template
    is returned again, with error messages injected.
    The field with the error must be a key on the error dict. The value is an
    optional message.
    """
    questionnaire = Questionnaire(questionnaire_uuid)
    error = {}
    if "email" not in request.form or request.form["email"] == "":
        error["email"] = "Please enter an E-Mail."
        # TODO: check if email is valid
    for question_group in questionnaire.questiongroups:
        for question in question_group.questions:
            if ("question_" + question.uuid) not in request.form:
                error["question_" + question.uuid] = "Please choose a value."

    # control all qacs and generate possibly error containing templates
    qac_templates = []
    for qac_module in questionnaire.get_qac_modules():
        errors = qac_module.control()
        qac_templates.append(qac_module.get_survey_template(errors))
        if errors != {}:
            # Just set any value to true, so that the template is rendered
            error["qac"] = True

    if error != {}:
        try:
            questionnaire = Questionnaire(questionnaire_uuid)
            return render_template(
                "survey_survey.html",
                uuid=questionnaire_uuid,
                questionnaire=questionnaire,
                qac_templates=qac_templates,
                values=request.form,
                error=error
            )
        except ObjectDoesntExistException as _:
            return make_response(redirect("/"))

    data_subject = DataSubject.one_from_query({"email_hash": request.form["email"]})
    if data_subject is None:
        data_subject = DataSubject()
        data_subject.email = request.form["email"]

    answer_overwritten = False
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
                question.add_question_result(current_answer)
            else:
                answer_overwritten = True
            current_answer.answer_value = request.form[
                "question_" + question.uuid]
            question.statistic.update()
    if not answer_overwritten:
        questionnaire.answer_count += 1

    return render_template("survey_thanks.html", email=request.form["email"])


@app.route("/survey/<string:questionnaire_uuid>/confirm/<string:confirmation_token>")
def survey_confirm_submission(questionnaire_uuid, confirmation_token):
    pass

@app.route("/disclaimer")
def disclaimer():
    return render_template("home_disclaimer.html")


# APIs

@app.route("/api/survey", methods=["GET"])
def api_survey_list():
    if g._current_user is not None:
        surveys = g._current_user.surveys
    else:
        surveys = Survey.many_from_query({})
    return make_response(jsonify(surveys))


@app.route("/api/survey", methods=["Post"])
def api_survey_create():
    data = request.get_json()
    survey = Survey.create_survey(data["name"])

    if g._current_user is not None:
        g._current_user.surveys.add(survey)

    return make_response(jsonify({
        "result": "Survey created.",
        "survey": survey
    }))


@app.route("/api/survey", methods=["PUT"])
def api_survey_update():
    data = request.get_json()
    try:
        survey = Survey(data["uuid"])

        if g._current_user is not None and survey not in g._current_user.surveys:
            return make_response(jsonify({
                "result": "error",
                "error": "Survey with given uuid does not belong to you."
            }), 400)

        survey.name = data["name"]
        return make_response(jsonify({
            "result": "Survey updated.",
            "survey": survey
        }))
    except ObjectDoesntExistException as e:
        return make_response(jsonify({
            "result": "error",
            "error": "Survey doesn't exist."
        }), 400)


@app.route("/api/survey", methods=["DELETE"])
def api_survey_delete():
    data = request.get_json()
    try:
        survey = Survey(data["uuid"])
        if g._current_user is not None and survey not in g._current_user.surveys:
            return make_response(jsonify({
                "result": "error",
                "error": "Survey with given uuid does not belong to you."
            }), 400)
        # TODO: delete subobjects
        survey.remove()
        return make_response(jsonify({
            "result": "Survey deleted."
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Survey doesn't exist."
        }), 400)


@app.route("/api/questionnaire/<string:questionnaire_uuid>", methods=["GET"])
def api_questionnaire_get_single(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        return make_response(jsonify(questionnaire))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/questionnaire/<string:questionnaire_uuid>/dl/csv",
           methods=["GET"])
def api_questionnaire_download_csv(questionnaire_uuid):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["question_group", "question_text", "answer_value"])
        questionnaire = Questionnaire(questionnaire_uuid)
        for question_group in questionnaire.questiongroups:
            for question in question_group.questions:
                for result in question.results:
                    writer.writerow([question_group.name,
                                     question.text,
                                     result.answer_value])

        response = make_response(output.getvalue())
        response.headers[
            "Content-Disposition"] = "attachment; filename=" + questionnaire_uuid + ".csv"
        response.headers["Content-type"] = "text/csv"

        return response
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/questionnaire", methods=["POST"])
def api_questionnaire_create():
    data = request.get_json()
    try:
        survey = Survey(data["survey"])
        if g._current_user is not None and survey not in g._current_user.surveys:
            return make_response(jsonify({
                "result": "error",
                "error": "Survey with given uuid does not belong to you."
            }), 400)
        if "template" in data["questionnaire"]:
            questionnaire = survey.add_new_questionnaire_from_template(
                data["questionnaire"]["name"],
                data["questionnaire"]["description"],
                data["questionnaire"]["template"]
            )
        else:
            questionnaire = survey.add_new_questionnaire(
                data["questionnaire"]["name"],
                data["questionnaire"]["description"]
            )
        return make_response(jsonify({
            "result": "Questionnaire created.",
            "questionnaire": questionnaire
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Survey doesn't exist."
        }), 400)
    except DuplicateQuestionnaireNameException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire with name \"" + data["questionnaire"][
                "name"] + "\" already exists."
        }), 400)


@app.route("/api/questionnaire", methods=["PUT"])
def api_questionnaire_update():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["uuid"])
        if "name" in data:
            questionnaire.name = data["name"]
        if "description" in data:
            questionnaire.description = data["description"]
        return make_response(jsonify({
            "result": "Questionnaire updated.",
            "questionnaire": questionnaire
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/questionnaire", methods=["DELETE"])
def api_questionnaire_delete():
    data = request.get_json()
    try:
        survey = Survey(data["survey"])
        if g._current_user is not None and survey not in g._current_user.surveys:
            return make_response(jsonify({
                "result": "error",
                "reason": "Survey with given uuid does not belong to you."
            }), 400)
        questionnaire = Questionnaire(data["uuid"])
        survey.remove_questionnaire(questionnaire)
        return make_response(jsonify({
            "result": "Questionnaire deleted."
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/qac_module", methods=["GET"])
def api_qac_modules():
    return make_response({
        "qacModules": ["AGBQAC"]  # TODO: Enumerate somewhere else
    })


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["POST"]
)
def api_qac_enable(questionnaire_uuid, qac_name):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        qac_module = create_qac_module(qac_name)
        if qac_module is None:
            return make_response(jsonify({
                "result": "error",
                "error": "QACModule \"" + qac_name + "\" doesn't exist."
            }), 400)
        questionnaire.add_qac_module(qac_module)
        return make_response({
            "result": "QACModule \"" + qac_name + "\" added to questionnaire.",
            "questionnaire": jsonify(questionnaire)
        })
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["PUT"]
)
def api_qac_configure(questionnaire_uuid, qac_name):
    data = request.get_json()
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        qac_module = questionnaire.get_qac_module(qac_name)
        if qac_module is None:
            return make_response(jsonify({
                "result": "error",
                "error": "QACModule \"" + qac_name + "\" doesn't exist on " +
                          "the requested questionnaire."
            }), 400)

        missing_params = []
        for key in qac_module.get_required_config_fields():
            if key not in data:
                missing_params.append(key)

        if missing_params != []:
            return make_response(jsonify({
                "result": "error",
                "error": "Parameters were missing; QACModule \"" + qac_name +
                          "\" was not updated.",
                "missingParams": missing_params
            }), 400)

        for key in qac_module.get_required_config_fields():
            qac_module.set_config_value(key, data[key])

        return make_response({
            "result": "QACModule \"" + qac_name + "\" updated.",
            "qacModule": jsonify(qac_module)
        })
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["DELETE"]
)
def api_qac_disable(questionnaire_uuid, qac_name):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
        questionnaire.remove_qac_module(qac_name)
        return make_response({
            "result": "QACModule \"" + qac_name + "\" removed from questionna" +
                      "ire.",
            "questionnaire": jsonify(questionnaire)
        })
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)


@app.route("/api/question_group", methods=["POST"])
def api_questiongroup_create():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["questionnaire"])
        question_group = questionnaire.add_question_group(data["name"])
        questionnaire.questiongroups.add(question_group)
        return make_response(jsonify({
            "result": "QuestionGroup created.",
            "question_group": question_group
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Questionnaire doesn't exist."
        }), 400)
    except DuplicateQuestionGroupNameException:
        return make_response(jsonify({
            "result": "error",
            "error": "QuestionGroup with name \"" +
                      data["name"] + "\" already exists."
        }), 400)


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
        return make_response(jsonify({
            "result": "QuestionGroup updated.",
            "question_group": question_group
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "QuestionGroup doesn't exist."
        }), 400)


@app.route("/api/question_group", methods=["DELETE"])
def api_questiongroup_delete():
    data = request.get_json()
    try:
        question_group = QuestionGroup(data["uuid"])
        questionnaire = Questionnaire(data["questionnaire"])
        questionnaire.questiongroups.remove(question_group)
        # TODO: delete subobjects. MEMORY LEAK
        question_group.remove()
        return make_response(jsonify({
            "result": "QuestionGroup deleted."
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "QuestionGroup doesn't exist."
        }), 400)


@app.route("/api/question", methods=["POST"])
def api_question_create():
    data = request.get_json()
    try:
        questionnaire = Questionnaire(data["questionnaire"])
        question_group = QuestionGroup(data["question_group"])

        try:
            question = questionnaire.add_question_to_group(question_group,
                                                           data["text"])
            return make_response(jsonify({
                "result": "Question created.",
                "question": question
            }))
        except DuplicateQuestionNameException:
            return make_response(jsonify({
                "result": "error",
                "error": "A Question with name \"" + data["text"] + "\" alrea" +
                         "dy exists on QuestionGroup \"" + question_group.name +
                         "\"."
            }), 400)
    except (ObjectDoesntExistException, QuestionGroupNotFoundException):
        return make_response(jsonify({
            "result": "error",
            "error": "QuestionGroup doesn't exist."
        }), 400)


@app.route("/api/question", methods=["PUT"])
def api_question_update():
    data = request.get_json()
    try:
        question = Question(data["uuid"])
        question.text = data["text"]
        return make_response(jsonify({
            "result": "Question updated.",
            "question": Question
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Question doesn't exist."
        }), 400)


@app.route("/api/question", methods=["DELETE"])
def api_question_delete():
    data = request.get_json()
    try:
        question = Question(data["uuid"])
        question_group = QuestionGroup(data["question_group"])
        questionnaire = Questionnaire(data["questionnaire"])
        questionnaire.remove_question_from_group(question_group, question)
        # TODO: remove all answers to deleted question
        return make_response(jsonify({
            "result": "Question deleted."
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Question doesn't exist."
        }), 400)


@app.route("/api/question/<string:question_uuid>/statistic", methods=["GET"])
def api_question_statistic(question_uuid):
    try:
        question = Question(question_uuid)
        return make_response(jsonify(question.statistic))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Question doesn't exist."
        }), 400)


@app.route("/api/account/current", methods=["GET"])
def api_account_current():
    if g._current_user:
        return make_response(jsonify(
            g._current_user
        ))
    else:
        return make_response(jsonify({
            "result": "error",
            "error": "No user logged in."
        }), 404)


@app.route("/api/account/<string:account_uuid>", methods=["GET"])
def api_account(account_uuid: str):
    try:
        return make_response(jsonify(
            DataClient(account_uuid)
        ))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Account doesn't exist."
        }), 404)


@app.route("/api/account/<string:account_uuid>", methods=["PUT"])
def api_account_update(account_uuid: str):
    data = request.get_json()
    try:
        client = DataClient(account_uuid)

        if "email" in data:
            client.email = data["email"]
        if "locale" in data and data["locale"] in Language:
            client.locale = data["locale"]

        return make_response(jsonify({
            "result": "Account updated.",
            "account": client
        }))
    except ObjectDoesntExistException:
        return make_response(jsonify({
            "result": "error",
            "error": "Account doesn't exist."
        }), 404)


@app.route("/test/runall", methods=["POST"])
def api_test_runall():
    # FIXME: remove (WHOLE METHOD) in production
    # if g._current_user is None:
    #    return abort(403)

    return make_response(jsonify({
        "result": test.run_all()
    }))
