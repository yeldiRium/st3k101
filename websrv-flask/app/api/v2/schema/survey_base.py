from marshmallow import fields

from api.v2.schema import RESTFulSchema
from api.v2.schema.fields import enum_field
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


def available_languages(item):
    return []  # TODO


class SurveyBaseSchema(RESTFulSchema):
    original_language = enum_field(BabelLanguage, dump_only=True)
    available_languages = fields.Function(available_languages,
                                          dump_only=True)
