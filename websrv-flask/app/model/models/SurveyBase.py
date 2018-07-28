from abc import abstractmethod
from typing import Dict, List, Union

from auth.users import current_user
from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType, translation_hybrid_updated, property_updated
from model import db
from model.models.OwnershipBase import OwnershipBase


__author__ = "Noah Hummel"


class SurveyBase(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'survey_base'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _template = db.Column(db.Boolean, default=False)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    @property
    @abstractmethod
    def reference_id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        raise NotImplementedError

    @property
    @abstractmethod
    def available_languages(self) -> List[BabelLanguage]:
        raise NotImplementedError

    @property
    @abstractmethod
    def shadow(self):
        raise NotImplementedError  # TODO: implement in child classes

    @property
    @abstractmethod
    def tracker_args(self) -> Dict[str, TrackingType]:
        raise NotImplementedError

    def __setattr__(self, key, value):
        """
        Hook for activity tracking
        """
        if key not in self.tracker_args.keys():
            object.__setattr__(self, key, value)
            return

        if hasattr(self, key):
            previous = getattr(self, key)
        else:
            previous = None
        object.__setattr__(self, key, value)

        key = _(key)  # translate property name if possible

        signal = None
        if self.tracker_args[key] == TrackingType.Primitive:
            signal = property_updated
        elif self.tracker_args[key] == TrackingType.TranslationHybrid:
            signal = translation_hybrid_updated

        signal.send(
            self,
            property_name=key,
            previous_value=previous,
            new_value=value
        )

    def __init__(self, **kwargs):
        super(SurveyBase, self).__init__(**kwargs)
        self.owners.append(current_user())

    def accessible_by(self, party):
        return super(SurveyBase, self).accessible_by(party) or self.template

    def modifiable_by(self, party):
        return super(SurveyBase, self).accessible_by(party)
