from marshmallow import Schema, fields


__author__ = "Noah Hummel"


class RESTFulSchema(Schema):
    id = fields.Int(dump_only=True)
