from marshmallow import Schema, fields

from framework.importer.schema.Dimension import DimensionImportSchema
from framework.importer.schema.fields import small_enum_field, I15dString
from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class QuestionnaireImportSchema(Schema):
    name = I15dString(required=True)
    description = I15dString(required=True)
    available_languages = fields.List(small_enum_field(BabelLanguage, required=True), required=True)
    original_language = small_enum_field(BabelLanguage, required=True)
    template = fields.Boolean(default=False)
    reference_id = fields.String(default=None)
    dimensions = fields.List(fields.Nested(DimensionImportSchema, required=True), required=True)
