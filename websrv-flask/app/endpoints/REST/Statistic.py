from flask import g
from flask.json import jsonify

from framework.internationalization import _
from framework import make_error
from framework.services import update_dirty_statistics
from main import app


@app.route("/api/statistics/update", methods=["POST"])
def update_statistics():
    """
    Updates all dirty QuestionStatistics which the currently logged in user can
    access.
    :return:
    """
    if g._current_user is None:
        return make_error(_("Lacking credentials"), 403)
    count = update_dirty_statistics()
    return jsonify({
        "result": "Statistics updated",
        "count": count
    })
