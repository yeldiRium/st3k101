from marshmallow import Schema, fields

from api.schema.fields import enum_field
from api.utils.ResourceBroker import ResourceBroker
from framework.internationalization.babel_languages import BabelLanguage
from model.models.TrackerEntry import PropertyUpdatedTrackerEntry, TranslatedPropertyUpdatedTrackerEntry, \
    ItemAddedTrackerEntry, ItemRemovedTrackerEntry, QuestionnaireRemovedTrackerEntry

__author__ = "Noah Hummel"


class TrackerEntrySchema(Schema):
    type = fields.Function(lambda o: o.__class__.__name__)
    id = fields.Integer()
    dataclient_email = fields.Email()
    timestamp = fields.DateTime()


class PropertyUpdatedTrackerEntrySchema(TrackerEntrySchema):
    item_name = fields.String()
    item_type = fields.Function(lambda o: o.item.__class__.__name__)
    item_href = fields.Function(lambda o: ResourceBroker.url_for(o.item))
    property_name = fields.String()
    previous_value = fields.String()
    new_value = fields.String()


class TranslatedPropertyUpdatedTrackerEntrySchema(PropertyUpdatedTrackerEntrySchema):
    language = enum_field(BabelLanguage)


class ItemAddedTrackerEntrySchema(TrackerEntrySchema):
    parent_item_name = fields.String()
    added_item_name = fields.String()
    parent_item_type = fields.Function(lambda o: o.parent_item.__class__.__name__)
    added_item_type = fields.Function(lambda o: o.added_item.__class__.__name__)
    parent_item_href = fields.Function(lambda o: ResourceBroker.url_for(o.parent_item))
    added_item_href = fields.Function(lambda o: ResourceBroker.url_for(o.added_item))


class ItemRemovedTrackerEntrySchema(TrackerEntrySchema):
    parent_item_name = fields.String()
    parent_item_type = fields.Function(lambda o: o.parent_item.__class__.__name__)
    removed_item_name = fields.String()
    parent_item_href = fields.Function(lambda o: ResourceBroker.url_for(o.parent_item))


class QuestionnaireRemovedTrackerEntrySchema(TrackerEntrySchema):
    questionnaire_name = fields.String()


TRACKER_ENTRY_MAPPING = {
    PropertyUpdatedTrackerEntry: PropertyUpdatedTrackerEntrySchema,
    TranslatedPropertyUpdatedTrackerEntry: TranslatedPropertyUpdatedTrackerEntrySchema,
    ItemAddedTrackerEntry: ItemAddedTrackerEntrySchema,
    ItemRemovedTrackerEntry: ItemRemovedTrackerEntrySchema,
    QuestionnaireRemovedTrackerEntry: QuestionnaireRemovedTrackerEntrySchema
}


def serialize_mixed_list(items, mapping):
    out = []
    schemas = dict()
    for i in items:
        t = type(i)
        if t not in schemas:
            schemas[t] = mapping[type(i)]()
        out.append(schemas[t].dump(i).data)
    return out
