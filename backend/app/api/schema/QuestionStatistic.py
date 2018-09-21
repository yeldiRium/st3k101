from marshmallow import Schema, fields

from framework.dependency_injection import ResourceBroker

__author__ = "Noah Hummel"


class QuestionStatisticSchema(Schema):
    smallest = fields.Integer()
    biggest = fields.Integer()
    q1 = fields.Float()
    q2 = fields.Float()
    q3 = fields.Float()
    n = fields.Integer()
    question_text = fields.Function(lambda s: s.question.text)
    question_href = fields.Function(lambda s: ResourceBroker.url_for(s.question))
    question_id = fields.Function(lambda s: s.question_id)
    question_range_start = fields.Function(lambda s: s.question.range_start)
    question_range_end = fields.Function(lambda s: s.question.range_end)
