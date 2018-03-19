from flask import g
from flask.json import jsonify

from framework.internationalization import _
from framework import make_error
from framework.services import update_dirty_statistics, update_all_statistics
from main import app


@app.route("/api/statistics/update", methods=["POST"])
def update_statistics():
    """
    Parameters:
        None

    Updates the statistics for all Questions that have unprocessed results.

    Response Codes:
        200: Dirty Questions successfully updated.
        403: No user is logged in.

    Response Class:
        200: {
            "count": Number of updated questions.
            "result": "Statistics updated."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    count = update_dirty_statistics()
    return jsonify({
        "result": _("Statistics updated."),
        "count": count
    })

@app.route("/api/statistics/update/force", methods=["POST"])
def force_update_statistics():
    """
    Parameters:
        None

    Updates the statistics for all Questions. Froces update, even if nothing
    has changed since the last update.

    Response Codes:
        200: Questions successfully updated.
        403: No user is logged in.

    Response Class:
        200: {
            "count": Number of updated questions.
            "result": "Statistics updated."
        }
        403: {
            "error": "Lacking credentials",
            "result": "error"
        }
    """
    """
    Updates all QuestionStatistics which the currently logged in user can
    access.
    :return:
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    count = update_all_statistics()
    return jsonify({
        "result": _("Statistics updated"),
        "count": count
    })
