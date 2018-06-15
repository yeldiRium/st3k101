from enum import Enum, auto

from flask import g

from framework.signals import app_signals
from model.SQLAlchemy import db
from model.SQLAlchemy.models.TrackerEntry import PrimitiveTrackerEntry, TranslationTrackerEntry, \
    RelationshipAddedTrackerEntry, RelationshipRemovedTrackerEntry, RelationshipAction, ItemDeletedTrackerEntry

__author__ = "Noah Hummel"


class TrackingType(Enum):
    Primitive = auto()
    TranslationHybrid = auto()
    RelationShip = auto()


class TrackingArg(Enum):
    Accumulate = auto()


primitive_property_updated = app_signals.signal('primitive_property_updated')
translation_hybrid_updated = app_signals.signal('translation_hybrid_updated')
relationship_updated = app_signals.signal('relationship_updated')
item_deleted = app_signals.signal('item_deleted')


@primitive_property_updated.connect
def log_primitive(sender, key=None, previous_value=None, new_value=None, person=None,
                  tracker_args=None):
    if previous_value is None:
        return

    if TrackingArg.Accumulate in tracker_args:
        previous_entries = PrimitiveTrackerEntry.query\
            .filter_by(sender=sender, attribute_name=key)
        for p in previous_entries:
            db.session.delete(p)

    te = PrimitiveTrackerEntry(sender, person, key, previous_value, new_value)
    db.session.add(te)

    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@translation_hybrid_updated.connect
def log_translation(sender, key=None, previous_value=None, new_value=None, person=None,
                    tracker_args=None):
    if previous_value is None:
        return

    if TrackingArg.Accumulate in tracker_args:
        previous_entries = TranslationTrackerEntry.query\
            .filter_by(sender=sender, attribute_name=key, language=g._language)
        for p in previous_entries:
            db.session.delete(p)

    te = TranslationTrackerEntry(sender, person, key, previous_value, new_value)
    db.session.add(te)

    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@relationship_updated.connect
def log_relationship(
        sender,
        relationship_name: str=None,
        action: RelationshipAction =None,
        related_object=None,
        person=None,
        tracker_args=None):
    if tracker_args:
        if TrackingArg.Accumulate in tracker_args:
            import sys
            print("[WARNING] TrackingArg.Accumulate set on relationship, this will "
                  "have no effect.", file=sys.stderr)

    if action == RelationshipAction.Add:
        te = RelationshipAddedTrackerEntry(sender, person, relationship_name,
                                           related_object)
    elif action == RelationshipAction.Remove:
        te = RelationshipRemovedTrackerEntry(sender, person, relationship_name,
                                             related_object)
    else:
        return

    db.session.add(te)
    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@item_deleted.connect
def log_questionnaire_deleted(sender, person):
    te = ItemDeletedTrackerEntry(sender, person)
    db.session.add(te)

    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)
