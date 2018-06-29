from abc import abstractmethod
from typing import List

from flask import g
from marshmallow import fields, missing, post_dump

from api.v2.schema import RESTFulSchema
from api.v2.schema.dataclient import DataClientSchema
from api.v2.schema.fields import enum_field
from auth.users import current_user
from framework.internationalization.babel_languages import BabelLanguage
from model.SQLAlchemy.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


class SurveyBaseSchema(RESTFulSchema):
    original_language = enum_field(BabelLanguage, dump_only=True)

    reference_id = fields.String()
    template = fields.Boolean()
    current_language = fields.Method('get_current_language', dump_only=True)
    available_languages = fields.List(enum_field(BabelLanguage), dump_only=True)
    shadow = fields.Boolean(dump_only=True)
    shadow_href = fields.Method('build_shadow_href', dump_only=True)
    owners = fields.Nested(DataClientSchema(only=("id", "href")), many=True,
                           dump_only=True)

    def get_current_language(self, obj):
        current_language = g._language
        if current_language not in obj.available_languages:
            current_language = obj.original_language
        return {
            'item_id': current_language.name,
            'value': current_language.value
        }

    def build_shadow_href(self, obj: SurveyBase):
        if not obj.shadow:
            return missing
        return super(SurveyBaseSchema, self).build_href(obj.concrete)

    @classmethod
    def get_private(cls) -> List[str]:
        if hasattr(cls, '__private__'):
            return cls.__private__
        return []

    @post_dump(pass_original=True, pass_many=False)
    def strip_private_fields(self, data, original_data: SurveyBase = None):

        def _strip(d):
            for k in self.get_private():
                del d[k]
            return d

        if isinstance(original_data, list):
            for od in original_data:
                if od.id == data['id']:
                    original_data = od
                    break

        if not original_data.modifiable_by(current_user()):
            return _strip(data)
