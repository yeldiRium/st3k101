from marshmallow import Schema, fields

from api.dependency_injection import ResourceBroker

__author__ = "Noah Hummel"


class RESTFulSchema(Schema):
    id = fields.Int(dump_only=True)
    href = fields.Method('build_href', dump_only=True)

    def build_href(self, obj):
        return ResourceBroker.url_for(obj)
