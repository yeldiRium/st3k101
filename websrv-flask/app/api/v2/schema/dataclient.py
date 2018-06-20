from typing import Type

from flask_restful import Resource
from marshmallow import fields

from api.v2.schema import RESTFulSchema
from api.v2.schema.fields import enum_field
from auth.roles import Role
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class DataClientSchema(RESTFulSchema):
    email = fields.Email(required=True)
    language = enum_field(BabelLanguage)
    roles = fields.List(enum_field(Role))
    password = fields.String(load_only=True, required=True)

    def __init__(self, resource: Type[Resource], *args, **kwargs):
        if 'context' not in kwargs:
            kwargs['context'] = dict()
        kwargs['context'] = {**kwargs['context'], **{'resource': resource}}
        super(RESTFulSchema, self).__init__(*args, **kwargs)
