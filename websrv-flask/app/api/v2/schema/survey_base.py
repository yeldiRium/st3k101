from marshmallow import Schema, fields, ValidationError
from urllib.parse import urljoin

from api.v2 import api
from api.v2.schema.fields import enum_field
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


def item_href(item, context):
    if 'resource' not in context:
        raise ValidationError('You have to provide a resource in the context'
                              'of a SurveyBase instance in order to serialize.')
    return api.url_for(context['resource']) + '/' + str(item.id)


def available_languages(item):
    return []  # TODO


class SurveyBaseSchema(Schema):
    id = fields.Int(dump_only=True)
    href = fields.Function(item_href, dump_only=True)
    original_language = enum_field(BabelLanguage, dump_only=True)
    available_languages = fields.Function(available_languages,
                                          dump_only=True)
