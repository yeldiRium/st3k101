from marshmallow import fields, Schema

from api.v2.schema.dimension import DimensionSchema
from api.v2.schema.qacmodule import QACModuleSchema
from api.v2.schema.survey_base import SurveyBaseSchema
from model.SQLAlchemy.models.Questionnaire import ShadowQuestionnaire

__author__ = "Noah Hummel"


class QuestionnaireSchema(SurveyBaseSchema):
    published = fields.Boolean()
    allow_embedded = fields.Boolean()
    xapi_target = fields.String(allow_none=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    dimensions = fields.Nested(DimensionSchema, many=True, dump_only=True)
    qac_modules = fields.Nested(QACModuleSchema, many=True, dump_only=True)
    shadow = fields.Method('get_is_shadow', dump_only=True)

    def get_is_shadow(self, obj):
        return isinstance(obj, ShadowQuestionnaire)


class ShadowQuestionnaireSchema(Schema):
    id = fields.Integer()
