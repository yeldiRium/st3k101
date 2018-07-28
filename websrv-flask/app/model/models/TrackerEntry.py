from datetime import datetime

from flask import g
from sqlalchemy.orm import backref

from framework.internationalization.babel_languages import BabelLanguage
from model import db, MUTABLE_HSTORE
from model.models.DataClient import DataClient
from model.models.OwnershipBase import OwnershipBase
from utils import ellipse


class TrackerEntry(OwnershipBase):
    """
    Base class for all tracker entries.
    Stores timestamp of the event and DataClient who
    triggered the event.
    """
    id = db.Column(
        db.Integer,
        db.ForeignKey(OwnershipBase.id, ondelete='CASCADE'),
        primary_key=True
    )

    # polymorphic config
    __tablename__ = 'tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    timestamp = db.Column(db.DateTime)
    dataclient_email = db.Column(db.String(100))

    def __init__(self, dataclient: DataClient, **kwargs):
        super(TrackerEntry, self).__init__(**kwargs)
        self.timestamp = datetime.now()
        self.dataclient_email = dataclient.email


class PropertyUpdatedTrackerEntry(TrackerEntry):
    """
    Stores the old and new values for a property of a certain
    survey item. Also stores a href to that item as well as the name of the
    item.
    """
    id = db.Column(db.Integer,
                   db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'property_updated_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    item_name = db.Column(db.String(50))
    property_name = db.Column(db.String(50))
    _values = db.Column(MUTABLE_HSTORE)

    # foreign keys
    item_id = db.Column(
        db.Integer,
        db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE')
    )

    # relationships
    item = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[item_id],
        backref=backref('property_updated_tracker_entries', cascade='all, delete')
    )

    def __init__(
        self,
        dataclient: DataClient,
        item_name: str,
        item: 'SurveyBase',
        property_name,
        previous_value,
        new_value,
        **kwargs
    ):
        super(PropertyUpdatedTrackerEntry, self).__init__(dataclient, **kwargs)
        self.item_name = ellipse(item_name, 50)
        self.item = item
        self.property_name = ellipse(property_name, 50)
        self._values = {'previous': str(previous_value), 'new': str(new_value)}

    @property
    def previous_value(self):
        return self._values['previous']

    @property
    def new_value(self):
        return self._values['new']


class TranslatedPropertyUpdatedTrackerEntry(PropertyUpdatedTrackerEntry):
    """
    Same as PropertyUpdatedTrackerEntry but used for columns that have multiple
    translations. Also stores the language of the updated property.
    """
    id = db.Column(
        db.Integer,
        db.ForeignKey(PropertyUpdatedTrackerEntry.id, ondelete='CASCADE'),
        primary_key=True
    )

    # polymorphic config
    __tablename__ = 'translated_property_updated_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    language = db.Column(db.Enum(BabelLanguage))

    def __init__(self, dataclient, item_name, item, property_name,
                 previous_value, new_value, **kwargs):
        super(TranslatedPropertyUpdatedTrackerEntry, self).__init__(
            dataclient,
            item_name,
            item,
            property_name,
            previous_value,
            new_value,
            **kwargs
        )
        self.language = g._language


class ItemAddedTrackerEntry(TrackerEntry):
    """
    TrackerEntry that indicates that a new item has been added to a survey.
    """
    id = db.Column(db.Integer,
                   db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'item_added_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    parent_item_name = db.Column(db.String(50))
    added_item_name = db.Column(db.String(50))

    # foreign keys
    parent_item_id = db.Column(
        db.Integer,
        db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE')
    )
    added_item_id = db.Column(
        db.Integer,
        db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE')
    )

    # relationships
    parent_item = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[parent_item_id],
        backref=backref('item_added_parent_tracker_entries', cascade='all, delete')

    )
    added_item = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[added_item_id],
        backref=backref('item_added_tracker_entries', cascade='all, delete')

    )

    def __init__(
        self,
        dataclient,
        parent_item_name: str,
        parent_item: 'SurveyBase',
        added_item_name: str,
        added_item: 'SurveyBase',
        **kwargs
    ):
        super(ItemAddedTrackerEntry, self).__init__(dataclient, **kwargs)
        self.parent_item_name = ellipse(parent_item_name, 50)
        self.added_item_name = ellipse(added_item_name, 50)
        self.parent_item = parent_item
        self.added_item = added_item


class ItemRemovedTrackerEntry(TrackerEntry):
    """
    TrackerEntry that indicates that an item has been removed from a survey.
    """
    id = db.Column(db.Integer,
                   db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'item_removed_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    parent_item_name = db.Column(db.String(50))
    removed_item_name = db.Column(db.String(50))

    # foreign keys
    parent_item_id = db.Column(
        db.Integer,
        db.ForeignKey('survey_base.id', onupdate='CASCADE', ondelete='CASCADE')
    )

    # relationships
    parent_item = db.relationship(
        'SurveyBase',
        uselist=False,
        foreign_keys=[parent_item_id],
        backref=backref('item_removed_parent_tracker_entries', cascade='all, delete')

    )

    def __init__(
        self,
        dataclient: DataClient,
        parent_item_name: str,
        parent_item: 'SurveyBase',
        removed_item_name: str,
        **kwargs
    ):
        super(ItemRemovedTrackerEntry, self).__init__(dataclient, **kwargs)
        self.parent_item_name = ellipse(parent_item_name, 50)
        self.removed_item_name = ellipse(removed_item_name, 50)
        self.parent_item = parent_item


class QuestionnaireRemovedTrackerEntry(TrackerEntry):
    """
    TrackerEntry that indicates that a Questionnaire was deleted by it's owner.
    """
    id = db.Column(db.Integer,
                   db.ForeignKey(TrackerEntry.id, ondelete='CASCADE'),
                   primary_key=True)

    # polymorphic config
    __tablename__ = 'questionnaire_removed_tracker_entry'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    questionnaire_name = db.Column(db.String(50))

    def __init__(self, dataclient: DataClient, questionnaire_name: str, **kwargs):
        super(QuestionnaireRemovedTrackerEntry, self).__init__(dataclient, **kwargs)
        self.questionnaire_name = ellipse(questionnaire_name, 50)
