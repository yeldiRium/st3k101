from marshmallow import fields, Schema

from api.v2.schema.dataclient import DataClientSchema
from api.v2.schema.dimension import DimensionSchema
from api.v2.schema.survey_base import SurveyBaseSchema
from model.SQLAlchemy.models.Questionnaire import ShadowQuestionnaire

__author__ = "Noah Hummel"


class QuestionnaireSchema(SurveyBaseSchema):
    email_whitelist = fields.List(fields.Email())
    email_blacklist = fields.List(fields.Email())
    password = fields.String()
    email_whitelist_enabled = fields.Boolean()
    email_blacklist_enabled = fields.Boolean()
    password_enabled = fields.Boolean()
    published = fields.Boolean()
    allow_embedded = fields.Boolean()
    xapi_target = fields.String(allow_none=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    dimensions = fields.Nested(DimensionSchema, many=True, dump_only=True)
    shadow = fields.Method('get_is_shadow', dump_only=True)
    owners = fields.Nested(DataClientSchema(only=("id", "href")), many=True, dump_only=True)

    __private__ = [
        'email_whitelist',
        'email_blacklist',
        'password',
        'email_whitelist_enabled',
        'email_blacklist_enabled',
        'password_enabled',
        'xapi_target',
        'allow_embedded'
    ]

    def get_is_shadow(self, obj):
        return isinstance(obj, ShadowQuestionnaire)


class ShadowQuestionnaireSchema(Schema):
    id = fields.Integer()
