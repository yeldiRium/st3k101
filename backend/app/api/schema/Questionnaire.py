from marshmallow import fields, Schema

from api.schema.DataClient import DataClientSchema
from api.schema.Dimension import DimensionSchema
from api.schema.SurveyBase import SurveyBaseSchema
from model.models.Questionnaire import ShadowQuestionnaire

__author__ = "Noah Hummel"


class QuestionnaireSchema(SurveyBaseSchema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    dimensions = fields.Nested(DimensionSchema, many=True, dump_only=True)

    shadow = fields.Method('get_is_shadow', dump_only=True)
    owners = fields.Nested(DataClientSchema(only=("id", "href")), many=True, dump_only=True)

    published = fields.Boolean()
    concluded = fields.Boolean()
    scheduled = fields.Boolean()
    begins = fields.DateTime()
    ends = fields.DateTime()

    password_enabled = fields.Boolean()
    email_whitelist_enabled = fields.Boolean()
    email_blacklist_enabled = fields.Boolean()
    password = fields.String()
    email_whitelist = fields.List(fields.Email())
    email_blacklist = fields.List(fields.Email())

    allow_embedded = fields.Boolean()
    allow_standalone = fields.Boolean()
    lti_consumer_key = fields.String(dump_only=True)

    xapi_target = fields.String(allow_none=True)

    __private__ = [
        *SurveyBaseSchema.get_private(),
        *[
            'published',
            'email_whitelist',
            'email_blacklist',
            'password',
            'email_whitelist_enabled',
            'email_blacklist_enabled',
            'password_enabled',
            'xapi_target',
            'allow_embedded',
            'lti_consumer_key'
        ]
    ]

    def get_is_shadow(self, obj):
        return isinstance(obj, ShadowQuestionnaire)


class ShadowQuestionnaireSchema(Schema):
    id = fields.Integer()
