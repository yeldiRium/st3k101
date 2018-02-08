"""
    All http endpoints that concern the rest-like api for Survey
"""

from flask import make_response, g
from flask.json import jsonify

from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException
from framework.internationalization import _
from main import app
from framework.flask_request import expect
from model.Survey import Survey


@app.route("/api/survey", methods=["GET"])
def api_survey_list():
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    return jsonify(g._current_user.surveys)
        # we previously listed out all surveys here.
        # This makes it, with the help of the other
        # endpoints, possible to list out all surveys
        # and all of their questions. We might need an endpoint to list
        # all surveys for admins of the platform, but
        # for this I would add a privilege check here.
        #surveys = Survey.many_from_query({})



@app.route("/api/survey", methods=["POST"])
@expect(('name', str))
def api_survey_create(name=''):

    # do not create a survey if the user is not logged in
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)

    survey = Survey.create_survey(name)
    g._current_user.surveys.add(survey)

    return jsonify({
        "result": _("Survey created."),
        "survey": survey
    })


@app.route("/api/survey", methods=["PUT"])
@expect(('uuid', str), ('name', str))
def api_survey_update(uuid="", name=""):

    try:
        survey = Survey(uuid)

        survey.name = name
        return jsonify({
            "result": _("Survey updated."),
            "survey": survey
        })

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)


@app.route("/api/survey", methods=["DELETE"])
@expect(('uuid', str))
def api_survey_delete(uuid=''):
    try:
        survey = Survey(uuid)
        # TODO: delete subobjects
        # strngdv @ 2018-02-07: fixed by cascading delete?
        g._current_user.surveys.discard(survey)
        survey.remove()

        return jsonify({"result": _("Survey deleted.")})

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)