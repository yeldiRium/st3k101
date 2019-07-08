import hashlib

from marshmallow import fields

from api.schema import RESTFulSchema
from api.schema.Question import QuestionSchema
from model.models.DataSubject import DataSubject

__author__ = "Noah Hummel"


class QuestionResponseSchema(RESTFulSchema):
    value = fields.Integer()
    question = fields.Nested(QuestionSchema)
    data_subject = fields.Method('anonymize_data_client')
    verified = fields.Boolean()

    def anonymize_data_client(self, obj):
        data_subject = next(filter(lambda ow: isinstance(ow, DataSubject), obj.owners))
        email = data_subject.email if data_subject else ""
        hasher = hashlib.sha256()
        hasher.update(email.encode('utf-8'))
        return hasher.digest().hex()
