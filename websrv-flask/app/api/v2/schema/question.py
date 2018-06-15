from marshmallow import fields

from api.v2.schema.survey_base import SurveyBaseSchema

__author__ = "Noah Hummel"


class QuestionSchema(SurveyBaseSchema):
    text = fields.String(required=True)
    range = fields.Integer(default=10)
