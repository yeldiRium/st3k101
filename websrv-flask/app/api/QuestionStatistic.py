from flask_restful import Resource, abort

from api import api
from api.Response import validate_resource_path
from api.schema.QuestionStatistic import QuestionStatisticSchema
from auth.users import current_user

__author__ = "Noah Hummel"


class QuestionStatisticResource(Resource):
    def get(self,
            questionnaire_id: int=None,
            dimension_id: int=None,
            question_id: int=None
            ):
        _, _, question = validate_resource_path(
            questionnaire_id,
            dimension_id,
            question_id
        )
        if not question.accessible_by(current_user()):
            abort(404)
        if not question.modifiable_by(current_user()):
            abort(403)
        return QuestionStatisticSchema().dump(question.statistic)


api.add_resource(
    QuestionStatisticResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>/statistic',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>/statistic',
    '/api/question/<int:question_id>/statistic'
)
