from marshmallow import fields

from api.v2.schema.fields import HexColor
from api.v2.schema.question import QuestionSchema
from api.v2.schema.survey_base import SurveyBaseSchema
from model.SQLAlchemy.models.Dimension import ShadowDimension

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