from datetime import datetime
from enum import Enum, auto

from flask import g

from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from model import db, MUTABLE_HSTORE
from model.models.OwnershipBase import OwnershipBase
from utils import ellipse

__author__ = "Noah Hummel"


class RelationshipAction(Enum):
    Add = auto()
    Remove = auto()


class TrackerEntry(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    timestamp = db.Column(db.DateTime)

    # foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', onupdate='CASCADE', ondelete='CASCADE'))

    # relationships
    sender = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[sender_id]
    )

    person = db.relationship(
        'Party',
        uselist=False,
        foreign_keys=[person_id]
    )

    def __init__(self, sender, person, **kwargs):
        super(TrackerEntry, self).__init__(**kwargs)
        self.sender = sender
        self.person = person
        self.timestamp = datetime.now()


class PrimitiveTrackerEntry(TrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'primitive_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _attribute_name = db.Column(db.String(50))
    _values = db.Column(MUTABLE_HSTORE)

    def __init__(self, sender, person, attribute_name, previous_value,
                 new_value, **kwargs):
        super(PrimitiveTrackerEntry, self).__init__(sender, person, **kwargs)
        self._attribute_name = attribute_name
        self._values = {'previous': str(previous_value), 'new': str(new_value)}

    @property
    def previous_value(self):
        return self._values['previous']

    @property
    def new_value(self):
        return self._values['new']

    @property
    def attribute_name(self):
        return _(self._attribute_name)


class TranslationTrackerEntry(PrimitiveTrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(PrimitiveTrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'translation_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    language = db.Column(db.Enum(BabelLanguage))

    def __init__(self, sender, person, attribute_name, previous_value,
                 new_value, **kwargs):
        super(TranslationTrackerEntry, self).__init__(sender, person,
                                                      attribute_name,
                                                      previous_value,
                                                      new_value, **kwargs)
        self.language = g._language


class RelationshipAddedTrackerEntry(TrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'relationship_added_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    _relationship_name = db.Column(db.String(50))

    # foreign keys
    related_object_id = db.Column(db.Integer, db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE'))

    related_object = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[related_object_id]
    )

    def __init__(self, sender, person, relationship_name, related_object,
                 **kwargs):
        super(RelationshipAddedTrackerEntry, self).__init__(sender, person, **kwargs)
        self._relationship_name = relationship_name
        self.related_object = related_object

    @property
    def relationship_name(self):
        return _(self._relationship_name)


class RelationshipRemovedTrackerEntry(TrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'relationship_removed_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    _relationship_name = db.Column(db.String(50))

    # foreign keys
    related_object_label = db.Column(db.String(50))

    def __init__(self, sender, person, relationship_name, related_object_label,
                 **kwargs):
        super(RelationshipRemovedTrackerEntry, self).__init__(sender, person, **kwargs)
        self._relationship_name = relationship_name

        if len(related_object_label) > 50:
            related_object_label = ellipse(related_object_label, 50)
        self.related_object_label = related_object_label

    @property
    def relationship_name(self):
        return _(self._relationship_name)


class ItemDeletedTrackerEntry(TrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'questionnaire_deleted_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}
