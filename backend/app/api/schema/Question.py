from marshmallow import fields, Schema

from api.schema.SurveyBase import SurveyBaseSchema
from model.models.Question import ShadowQuestion

__author__ = "Noah Hummel"


class QuestionSchema(SurveyBaseSchema):
    text = fields.String(required=True)
    range_start = fields.Integer(default=10)
    range_end = fields.Integer(default=0)
    shadow = fields.Method('is_shadow')

    def is_shadow(self, obj):
        return isinstance(obj, ShadowQuestion)


class ShadowQuestionSchema(Schema):
    id = fields.Integer(required=True)
