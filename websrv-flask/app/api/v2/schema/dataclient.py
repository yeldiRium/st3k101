from marshmallow import Schema, fields

from api.v2.schema.fields import enum_field
from auth.roles import Role
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class DataClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    language = enum_field(BabelLanguage)
    roles = enum_field(Role)
    password = fields.String(load_only=True, required=True)
