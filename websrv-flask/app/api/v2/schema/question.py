from marshmallow import fields

from api.v2.schema.survey_base import SurveyBaseSchema
from model.SQLAlchemy.models.Question import ShadowQuestion

__author__ = "Noah Hummel"


class QuestionSchema(SurveyBaseSchema):
    text = fields.String(required=True)
    range = fields.Integer(default=10)
    shadow = fields.Method('is_shadow')

    def is_shadow(self, obj):
        return isinstance(obj, ShadowQuestion)
