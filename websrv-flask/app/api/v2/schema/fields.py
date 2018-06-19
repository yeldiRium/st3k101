from marshmallow import fields, ValidationError

__author__ = "Noah Hummel"


def enum_field(some_enum, **kwargs):

    def is_in_enum(v):
        return any((v['name'] == i.name and v['value'] == i.value)
                   for i in some_enum)

    class EnumFieldClosure(fields.Field):
        def _serialize(self, value, attr, obj):
            if value not in some_enum:
                raise ValidationError('{} is not a valid {}.'.format(value, some_enum.__name__))
            return {'name': value.name, 'value': value.value}

        def _deserialize(self, value, attr, data):
            if not is_in_enum(value):
                raise ValidationError('{} is not a valid {}.'.format(value, some_enum.__name__))
            return some_enum[value['name']]

    return EnumFieldClosure(**kwargs)
