from marshmallow import Schema, fields

__author__ = "Noah Hummel"


class SmallDataSubjectSchema(Schema):
    email = fields.Email(required=True)


class DataSubjectQuerySchema(Schema):
    email = fields.String()
    moodle_username = fields.String()
    source = fields.String()


class DataSubjectSchema(Schema):
    email = fields.Email()
    lti_user_id = fields.String()
    moodle_username = fields.String()
    source = fields.String()
