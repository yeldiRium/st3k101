from flask_restful import Resource, abort

from api import api
from api.Response import validate_resource_path
from api.schema.QuestionStatistic import QuestionStatisticSchema
from auth.session import current_user
from model.models.Questionnaire import Questionnaire

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
            abort(403)
        if not question.modifiable_by(current_user()):
            abort(403)

        return QuestionStatisticSchema().dump(question.statistic)


class QuestionnaireStatisticsResource(Resource):
    def get(self, questionnaire_id: int=None):
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        if not questionnaire.accessible_by(current_user()):
            abort(403)
        if not questionnaire.modifiable_by(current_user()):
            abort(403)

        statistics = []
        for dimension in questionnaire.dimensions:
            for question in dimension.questions:
                statistics.append(question.statistic)

        return QuestionStatisticSchema(many=True).dump(statistics)


api.add_resource(
    QuestionStatisticResource,
    '/api/questionnaire/<int:questionnaire_id>/dimension/<int:dimension_id>/question/<int:question_id>/statistic',
    '/api/dimension/<int:dimension_id>/question/<int:question_id>/statistic',
    '/api/question/<int:question_id>/statistic'
)


api.add_resource(
    QuestionnaireStatisticsResource,
    '/api/questionnaire/<int:questionnaire_id>/statistics'
)
