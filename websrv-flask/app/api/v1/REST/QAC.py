"""
    All http endpoints that concern the rest-like api for QAC
"""

from flask import make_response, request, g
from flask.json import jsonify

from app import app
from framework import make_error
from framework.exceptions import QACAlreadyEnabledException
from framework.internationalization import _
from framework.ownership import owned
from model.SQLAlchemy import db

from model.SQLAlchemy.models.QAC.QACModules import QAC
from model.SQLAlchemy.models.Questionnaire import Questionnaire
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from view.views.QACModule import LegacyView
from view.views.Questionnaire import LegacyView as Questionnaire_LegacyView

__author__ = "Noah Hummel, Hannes Leutloff"


@app.route("/api/qac_module", methods=["GET"])
def api_qac_modules():
    """
    Parameters:
        None.

    Response Codes:
        200: Returns list of implemented QACModules.

    Response Class:
        200: {
                "qacModules": [
                    module name: String
                ]
            }
    """

    return jsonify({
        "qacModules": {qac.name: _(qac.value.get_qac_id()) for qac in QAC}
    })


@app.route(
    "/api/questionnaire/<int:questionnaire_uuid>/qac",
    methods=["GET"]
)
def api_questionnaire_list_qacs(questionnaire_uuid: int):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire whose qacs
            shall be listed.

    Response Codes:
        200: Returns the QAC list.
        403: If no user is logged in or the current user doesn't have access to
            the given Questionnaire.
        404: If the uuid does not belong to a Questionnaire.

    Response Class:
        200: [QACModule] (See GET
            /api/questionnaire/questionnaire_uuid/qac/qac_name)
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire.",
            "result": "error"
        }

    Explanation:
        The QAC type and QAC parameter type tell a lot about what kind of QAC
        each object is. Bot the description and name properties will tell even
        more about that.
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not owned(questionnaire):
        # only the owner can list the qacs of an Questionnaire via the api,
        # they're not serialized with questionnaire
        return make_error(_("Lacking credentials"), 403)

    return LegacyView.jsonify(questionnaire.get_qac_modules())


@app.route(
    "/api/questionnaire/<int:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["GET"]
)
def api_questionnaire_get_qac(questionnaire_uuid: int, qac_name: str):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire whose qac is
            requested.
        qac_name: String The name of the requested QACModule.

    Response Codes:
        200: Returns the QAC object.
        403: If no user is logged in or the current user doesn't have access to
            the given Questionnaire.
        404: If the uuid does not belong to a Questionnaire or the qac name does
            not belong to a QAC object on the Questionnaire.

    Response Class:
        200: QACMOdule: {
            "class": "model.query_access_control.QACModules." + qac type,
            "fields": {
                "description": DataString,
                "name": DataString,
                "parameters": [{
                    "class": "model.query_access_control." + qac parameter type,
                    "fields": {
                        "description": DataString,
                        "name": DataString
                    },
                    "uuid": String
                }]
            },
            "uuid": String
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such QAC.",
            "result": "error"
        }
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not owned(questionnaire):
        return make_error(_("Lacking credentials"), 403)

    try:
        QAC[qac_name]  # type: QACModule
    except KeyError:
        return make_error(_("No such QAC."), 404)

    qac_name = QAC[qac_name].value.get_qac_id()  # TODO use qac_ids in enum to begin with...

    qac_instance = questionnaire.get_qac_module_by_qac_id(qac_name)
    if qac_instance is None:
        return make_error(_("QAC is not enabled."), 404)

    return LegacyView.jsonify(qac_instance)


@app.route(
    "/api/questionnaire/<int:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["POST"]
)
def api_qac_enable(questionnaire_uuid: int, qac_name: str):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire in question.
        qac_name: String The name of the QACModule that shall be enabled. Has
            to be present in the returned list on /api/qac_module.

    Response Codes:
        200: The QACModule is enabled on the given Questionnaire.
        403: No user is logged in or the current user does not have permission
            to edit the given Questionnaire.
        404: qac_name is not a name for a valid QACModule or questionnaire_uuid
            does not belong to a Questionnaire.

    Response Class:
        200: {
            "questionnaire": Questionnaire
                (see GET /api/questionnaire/questionnaire_uuid)
            "result": "QACModule added to Questionnaire."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such QAC.",
            "result": "error"
        }
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)

    if not owned(questionnaire):
        return make_error(_("Lacking credentials"), 403)

    try:
        qac_module = QAC[qac_name].value
    except KeyError:
        return make_error(_("No such QAC."), 404)

    try:
        questionnaire.add_qac_module(qac_module())
    except QACAlreadyEnabledException:
        db.session.rollback()
        return make_error(_("QACModule is already enabled."))
    else:
        db.session.commit()
        return jsonify({
            "result": _("QACModule added to Questionnaire."),
            "questionnaire": Questionnaire_LegacyView.render(questionnaire)
        })


@app.route(
    "/api/questionnaire/<int:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["PUT"]
)
def api_qac_configure(questionnaire_uuid: int, qac_name: str):
    """
    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire in question.
        qac_name: String The name of the QACModule that shall be configured. Has
            to be present in the returned list on /api/qac_module.

        Data Body of Content-Type: "application/json":
            {
                QACParameter.name: "some_value"
            }

        Where all QACParameter.name have to be in the QACParameter list returned
        from GET /api/questionnaire/questionnaire_uuid/qac/qac_name.

    Response Codes:
        200: QACModule was either completely or partially configured. If it was
            only partially configured, the Response contains an error array.
        400: A parameter was missing and the QACModule was not updated.
        403: No user is logged in or the current user does not have permission
            to edit the given Questionnaire.
        404: qac_name is not a name for a valid QACModule or questionnaire_uuid
            does not belong to a Questionnaire.

    Response Class:
        200: {
            "errors": [String],
            "qacModule": QACModule (see
                GET /api/questionnaire/questionnaire_uuid/qac/qac_name),
            "result": "QACModule updated." / "Nothing updated."
                / "Partially updated."
        }
        400: {
            "error": "Missing parameter(s) " + list of QACParameter names
            "result": "error"
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such QAC." / "QAC {name} is not enabled.",
            "result": "error"
        }

    Explanation:
        If the Response Code is 200, three outcomes are possible: Everything
        went well and the module was configured / Everything went well any no-
        thing was changed / Some errors occured but some values were set.
        In the last case, the error list will contain detailed error reports.
    """
    request_data = request.get_json()

    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)
    if g._current_user != questionnaire.survey.data_client:
        return make_error(_("Lacking credentials"), 403)

    qac_module = questionnaire.get_qac_module_by_qac_id(qac_name)
    if qac_module is None:
        return make_error("QAC {} is not enabled.".format(qac_name), 404)

    updated_params = []
    errors = []

    missing_params = []
    for p in qac_module.parameters:
        if request_data is None or p.name_msgid not in request_data:
            missing_params.append("'{}'".format(p.name_msgid))
    if missing_params:
        return make_error(
            _("Missing parameter(s) ") + "{}".format(", ".join(missing_params)),
            400
        )

    for p in qac_module.parameters:
        err = qac_module.set_config_value(p.id, request_data[p.name_msgid])
        if err:
            errors.append({
                "parameter": p.name_msgid,
                "error": err
            })
        else:
            updated_params.append(p.name_msgid)

    if not updated_params:
        result = _("Nothing updated.")
    elif not errors:
        result = _("QACModule updated.")
    else:
        result = _("Partially updated.")

    db.session.commit()

    return make_response(jsonify({
        "result": result,
        "errors": errors,
        "qacModule": LegacyView.render(qac_module)
    }), 200)


@app.route(
    "/api/questionnaire/<int:questionnaire_uuid>/qac/<string:qac_name>",
    methods=["DELETE"]
)
def api_qac_disable(questionnaire_uuid: int, qac_name: str):
    """
    TODO: throws 500

    Parameters:
        questionnaire_uuid: String The uuid for the Questionnaire in question.
        qac_name: String The name of the QACModule that shall be disabled. Has
            to be present in the returned list on /api/qac_module.

    Response Codes:
        200: The QACModule is enabled on the given Questionnaire.
        400: The QACModule is already enabled.
        403: No user is logged in or the current user does not have permission
            to edit the given Questionnaire.
        404: qac_name is not a name for a valid QACModule or questionnaire_uuid
            does not belong to a Questionnaire.

    Response Class:
        200: {
            "questionnaire": Questionnaire
                (see GET /api/questionnaire/questionnaire_uuid)
            "result": "QACModule disabled."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
        404: {
            "error": "No such Questionnaire." / "No such QAC.",
            "result": "error"
        }
    """
    questionnaire = Questionnaire.query.get_or_404(questionnaire_uuid)
    qac_module = questionnaire.get_qac_module_by_qac_id(qac_name)

    if qac_module is None:
        return make_error(_("Not found."), 404)

    if g._current_user != questionnaire.survey.data_client:
        return make_error(_("Lacking credentials"), 403)

    questionnaire.qac_modules.remove(qac_module)
    db.session.commit()

    return jsonify({
        "result": _("QACModule disabled."),
        "questionnaire": Questionnaire_LegacyView.render(questionnaire)
    })
