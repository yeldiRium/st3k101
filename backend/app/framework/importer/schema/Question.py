from marshmallow import Schema, fields

from framework.importer.schema.fields import I15dString

__author__ = "Noah Hummel"


class QuestionImportSchema(Schema):
    text = I15dString(required=True)
    range_start = fields.Integer(default=1)
    range_end = fields.Integer(default=10)
    reference_id = fields.String(default=None)
    range_start_label = I15dString(required=True)
    range_end_label = I15dString(required=True)
