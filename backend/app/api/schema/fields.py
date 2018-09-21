from marshmallow import fields, ValidationError

from utils import check_color

__author__ = "Noah Hummel"


def is_in_enum(v, some_enum):
    return any((v['item_id'] == i.name and v['value'] == i.value)
               for i in some_enum)


def enum_field(some_enum, **kwargs):

    class EnumFieldClosure(fields.Field):
        def _serialize(self, value, attr, obj):
            if value not in some_enum:
                raise ValidationError('{} is not a valid {}.'.format(value, some_enum.__name__))
            return {'item_id': value.name, 'value': value.value}

        def _deserialize(self, value, attr, data):
            if 'item_id' not in value or 'value' not in value:
                raise ValidationError('Invalid enumerator format.')
            if not is_in_enum(value, some_enum):
                raise ValidationError('{} is not a valid {}.'.format(value, some_enum.__name__))
            return some_enum[value['item_id']]

    return EnumFieldClosure(**kwargs)


class HexColor(fields.Field):
    def _serialize(self, value, attr, obj):
        return value

    def _deserialize(self, value, attr, data):
        try:
            check_color(value)
        except ValueError as e:
            raise ValidationError(*e.args)
