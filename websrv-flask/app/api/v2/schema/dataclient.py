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
