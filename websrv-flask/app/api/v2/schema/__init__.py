from marshmallow import ValidationError, Schema, fields

from api.v2 import api

__author__ = "Noah Hummel"


def item_href(item, context):
    if 'resource' not in context:
        raise ValidationError('You have to provide a resource in the context'
                              'of a SurveyBase instance in order to serialize.')
    return api.url_for(context['resource']) + '/' + str(item.id)


class RESTFulSchema(Schema):
    id = fields.Int(dump_only=True)
    href = fields.Function(item_href, dump_only=True)
