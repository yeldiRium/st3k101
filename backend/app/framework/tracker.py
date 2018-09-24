from enum import Enum, auto

from flask import g

from framework.signals import (
    property_updated,
    translation_hybrid_updated,
    item_added,
    item_removed,
    questionnaire_removed
)
from model.models.TrackerEntry import (
    PropertyUpdatedTrackerEntry,
    TranslatedPropertyUpdatedTrackerEntry,
    ItemAddedTrackerEntry,
    ItemRemovedTrackerEntry,
    QuestionnaireRemovedTrackerEntry
)
from auth.session import current_user
from model import db

__author__ = "Noah Hummel"


class TrackingType(Enum):
    Primitive = auto()
    TranslationHybrid = auto()


@property_updated.connect
def track_property_updated(
    sender: 'SurveyBase',
    property_name=None,
    previous_value=None,
    new_value=None
):
    if previous_value is None:  # first time property is set
        return

    if previous_value == new_value:  # orly?
        return

    # remove previous entries for same property
    previous_entries = PropertyUpdatedTrackerEntry.query\
        .filter_by(item=sender, property_name=property_name)
    for p in previous_entries:
        db.session.delete(p)

    te = PropertyUpdatedTrackerEntry(
        dataclient=current_user(),
        item_name=sender.name,
        item=sender,
        property_name=property_name,
        previous_value=previous_value,
        new_value=new_value
    )
    db.session.add(te)

    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@translation_hybrid_updated.connect
def track_translation_hybrid_updated(
    sender: 'SurveyBase',
    property_name=None,
    previous_value=None,
    new_value=None
):
    if previous_value is None:
        return

    if previous_value == new_value:
        return

    previous_entries = TranslatedPropertyUpdatedTrackerEntry.query\
        .filter_by(item=sender, property_name=property_name, language=g._language)
    for p in previous_entries:
        db.session.delete(p)

    te = TranslatedPropertyUpdatedTrackerEntry(
        dataclient=current_user(),
        item_name=sender.name,
        item=sender,
        property_name=property_name,
        previous_value=previous_value,
        new_value=new_value
    )
    db.session.add(te)

    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@item_added.connect
def track_item_added(
    sender: 'SurveyBase',
    added_item: 'SurveyBase'=None
):
    te = ItemAddedTrackerEntry(
        dataclient=current_user(),
        parent_item_name=sender.name,
        parent_item=sender,
        added_item_name=added_item.name,
        added_item=added_item
    )
    db.session.add(te)
    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@item_removed.connect
def track_item_removed(
    sender: 'SurveyBase',
    removed_item_name: str=None
):
    te = ItemRemovedTrackerEntry(
        dataclient=current_user(),
        parent_item_name=sender.name,
        parent_item=sender,
        removed_item_name=removed_item_name
    )
    db.session.add(te)
    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)


@questionnaire_removed.connect
def track_questionnaire_removed(
    sender: 'SurveyBase'
):
    te = QuestionnaireRemovedTrackerEntry(
        dataclient=current_user(),
        questionnaire_name=sender.name
    )
    db.session.add(te)
    te.owners.extend(sender.owners)
    # make all people with a reference (shadow copy) of sender own the tracker
    # entry, so that the change will be shown in their feed
    if hasattr(sender, 'copies'):
        for copy in sender.copies:
            te.owners.extend(copy.owners)
