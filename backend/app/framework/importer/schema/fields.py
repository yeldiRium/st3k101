from marshmallow import fields

from framework.internationalization.babel_languages import BabelLanguage

__author__ = "Noah Hummel"


class I15dString(fields.Field):
    def _serialize(self, value, attr, obj):
        raise NotImplementedError

    def _deserialize(self, value, attr, data):
        if type(value) is not dict:
            return self.missing
        for lang, text in value.items():
            try:
                _ = BabelLanguage[lang]
            except (KeyError, ValueError):
                return self.missing
            return value

def small_enum_field(some_enum, key='name', **kwargs):

    class SmallEnumFieldClosure(fields.Field):
        def _serialize(self, value, attr, obj):
            raise NotImplementedError

        def _deserialize(self, value, attr, data):
            try:
                if key == 'name':
                    return some_enum[value]
                elif key == 'value':
                    return next((e for e in some_enum if e.value == value))
            except (KeyError, StopIteration):
                return self.missing

    return SmallEnumFieldClosure(**kwargs)
