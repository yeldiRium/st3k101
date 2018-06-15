from marshmallow import Schema, fields

__author__ = "Noah Hummel"


class SessionSchema(Schema):
    session_token = fields.String()


class LoginSchema(Schema):
    email = fields.Email()
    password = fields.String()
