from marshmallow import Schema, fields

from framework.importer.schema.Question import QuestionImportSchema
from framework.importer.schema.fields import I15dString

__author__ = "Noah Hummel"


class DimensionImportSchema(Schema):
    name = I15dString(required=True)
    reference_id =  fields.String(default=None)
    randomize_question_order = fields.Boolean(missing=False, required=True)
    questions = fields.List(fields.Nested(QuestionImportSchema))
