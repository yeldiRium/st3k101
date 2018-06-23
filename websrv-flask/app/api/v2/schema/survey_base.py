from flask import g
from marshmallow import fields

from api.v2.schema import RESTFulSchema
from api.v2.schema.fields import enum_field
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class SurveyBaseSchema(RESTFulSchema):
    original_language = enum_field(BabelLanguage, dump_only=True)

    reference_id = fields.String()
    template = fields.Boolean()
    current_language = fields.Method('get_current_language', dump_only=True)

    def get_current_language(self, obj):
        current_language = g._language
        language = current_language
        if current_language not in obj.available_languages:
            current_language = obj.original_language
        return {
            'item_id': current_language.name,
            'value': current_language.value
        }
