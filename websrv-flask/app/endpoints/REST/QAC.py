"""
    All http endpoints that concern the rest-like api for QAC
"""

from flask import make_response, request
from flask.json import jsonify

from businesslogic.QAC import QAC
from framework import make_error
from framework.exceptions import AccessControlException, \
    ObjectDoesntExistException, QACAlreadyEnabledException, \
    QACNotEnabledException
from framework.internationalization import _
from main import app
from model.Questionnaire import Questionnaire
from model.query_access_control.QACModule import QACModule


@app.route("/api/qac_module", methods=["GET"])
def api_qac_modules():
    return jsonify({
        "qacModules": [qac.name for qac in QAC]
    })


@app.route("/api/questionnaire/<string:questionnaire_uuid>/qac", methods=["GET"])
def api_questionnaire_list_qacs(questionnaire_uuid):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not questionnaire.accessible():
        # only the owner can list the qacs of an Questionnaire via the api,
        # they're not serialized with questionnaire
        return make_error(_("Lacking credentials"), 403)

    return jsonify(questionnaire.get_qac_modules())


@app.route("/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
           methods=["GET"])
def api_questionnaire_get_qac(questionnaire_uuid, qac_name):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)

    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not questionnaire.accessible():
        # again, only the owner may view qac parameters
        return make_error(_("Lacking credentials"), 403)

    try:
        qac_module = QAC[qac_name]  # type: QACModule

    except KeyError:
        return make_error(_("No such QAC."), 404)

    qac_instance = questionnaire.get_qac_module(qac_name)
    if qac_instance is None:
        return make_error(_("QAC is not enabled."), 404)

    return jsonify(qac_instance)


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["POST"]
)
def api_qac_enable(questionnaire_uuid, qac_name):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    try:
        qac_module = QAC[qac_name]  # type: QACModule
    except KeyError:
        return make_error(_("No such QAC."), 404)

    try:
        questionnaire.add_qac_module(qac_module.new())
        return jsonify({
            "result": _("QACModule added to questionnaire."),
            "questionnaire": jsonify(questionnaire)
        })
    except QACAlreadyEnabledException:
        return make_error(_("QACModule already enabled."), 400)


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["PUT"]
)
def api_qac_configure(questionnaire_uuid, qac_name):
    """
    Format of request data: 
    {
        QACParam.name: "some_value",
        ...
    }
    """
    request_data = request.get_json()

    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    qac_module = questionnaire.get_qac_module(qac_name)
    if qac_module is None:
        return make_error("QAC is not enabled.".format(qac_name), 404)

    updated_params = []
    errors = []

    for p in qac_module.parameters:
        if p.name not in request_data:
            return make_error(_("Missing parameter ") +"'{}'".format(p.name), 400)

    for p in qac_module.parameters:
        err = qac_module.set_config_value(p.uuid, request_data[p.name])
        if err:
            errors.append({
                "parameter": p.name,
                "error": err
            })
        else:
            updated_params.append(p.name)


    if not updated_params:
        status = 400
        result = _("Nothing updated.")

    elif not errors:
        status = 200
        result = _("QACModule updated.")

    else:
        status = 207
        result = _("Partially updated.")

    return make_response(jsonify({
            "result": result,
            "errors": errors,
            "qacModule": qac_module
        }), status)


@app.route(
    "/api/questionnaire/<string:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["DELETE"]
)
def api_qac_disable(questionnaire_uuid, qac_name):
    try:
        questionnaire = Questionnaire(questionnaire_uuid)
    except (AccessControlException, ObjectDoesntExistException):
        return make_error(_("Not found."), 404)

    if not questionnaire.accessible():
        return make_error(_("Lacking credentials"), 403)

    try:
        questionnaire.remove_qac_module(qac_name)
        return jsonify({
            "result": _("QACModule disabled."),
            "questionnaire": questionnaire
        })
    except QACNotEnabledException:
        return make_error(_("Not found."), 404)
