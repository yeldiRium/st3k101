from marshmallow import fields, Schema

from api.schema.Question import QuestionSchema
from api.schema.SurveyBase import SurveyBaseSchema
from model.models.Dimension import ShadowDimension

__author__ = "Noah Hummel"


class DimensionSchema(SurveyBaseSchema):
    name = fields.String(required=True)
    position = fields.Integer()
    randomize_question_order = fields.Boolean()
    questions = fields.Nested(QuestionSchema, many=True)
    shadow = fields.Method('is_shadow')

    def is_shadow(self, obj):
        return isinstance(obj, ShadowDimension)


class ShadowDimensionSchema(Schema):
    id = fields.Integer()
