from marshmallow import fields, Schema

from api.schema.fields import HexColor
from api.schema.Question import QuestionSchema
from api.schema.SurveyBase import SurveyBaseSchema
from model.models.Dimension import ShadowDimension

__author__ = "Noah Hummel"


class DimensionSchema(SurveyBaseSchema):
    name = fields.String(required=True)
    color = HexColor()
    text_color = HexColor()
    randomize_question_order = fields.Boolean()
    questions = fields.Nested(QuestionSchema, many=True)
    shadow = fields.Method('is_shadow')

    def is_shadow(self, obj):
        return isinstance(obj, ShadowDimension)


class ShadowDimensionSchema(Schema):
    id = fields.Integer()
