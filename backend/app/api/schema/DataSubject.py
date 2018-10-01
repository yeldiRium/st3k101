from marshmallow import Schema, fields

__author__ = "Noah Hummel"


class DataSubjectSchema(Schema):
    email = fields.Email(required=True)
