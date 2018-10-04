from marshmallow import Schema, fields

from api.schema.DataSubject import SmallDataSubjectSchema

__author__ = "Noah Hummel"


class QuestionSubmissionSchema(Schema):
    id = fields.Integer(required=True)
    value = fields.Integer(required=True)


class DimensionSubmissionSchema(Schema):
    id = fields.Integer(required=True)
    questions = fields.Nested(QuestionSubmissionSchema,
                              many=True, required=True)


class SubmissionSchema(Schema):
    data_subject = fields.Nested(SmallDataSubjectSchema, required=True)
    password = fields.String()
    captcha_token = fields.String(required=True)
    dimensions = fields.Nested(DimensionSubmissionSchema,
                               many=True, required=True)
