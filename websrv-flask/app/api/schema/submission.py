from marshmallow import Schema, fields

from api.schema.datasubject import DataSubjectSchema

__author__ = "Noah Hummel"


class QuestionSubmissionSchema(Schema):
    id = fields.Integer()
    value = fields.Integer()


class DimensionSubmissionSchema(Schema):
    id = fields.Integer(required=True)
    questions = fields.Nested(QuestionSubmissionSchema,
                              many=True, required=True)


class SubmissionSchema(Schema):
    data_subject = fields.Nested(DataSubjectSchema, required=True)
    password = fields.String()
    captcha_token = fields.String(required=True)
    dimensions = fields.Nested(DimensionSubmissionSchema,
                               many=True, required=True)
