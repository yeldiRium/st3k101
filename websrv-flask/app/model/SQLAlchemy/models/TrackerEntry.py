from datetime import datetime

from flask import g

from framework.internationalization.babel_languages import BabelLanguage
from model.SQLAlchemy import db, MUTABLE_HSTORE
from model.SQLAlchemy.models.OwnershipBase import OwnershipBase

__author__ = "Noah Hummel"


class TrackerEntry(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    timestamp = db.Column(db.DateTime)

    # foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('survey_base.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

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
    id = db.Column(db.Integer, db.ForeignKey(TrackerEntry.id),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'primitive_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    attribute_name = db.Column(db.String(50))
    _values = db.Column(MUTABLE_HSTORE)

    def __init__(self, sender, person, attribute_name, previous_value,
                 new_value, **kwargs):
        super(PrimitiveTrackerEntry, self).__init__(sender, person, **kwargs)
        self.attribute_name = attribute_name
        self._values = {'previous': previous_value, 'new':new_value}

    @property
    def previous_value(self):
        return self._values['previous']

    @property
    def new_value(self):
        return self._values['new']


class TranslationTrackerEntry(PrimitiveTrackerEntry):
    id = db.Column(db.Integer, db.ForeignKey(PrimitiveTrackerEntry.id),
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
