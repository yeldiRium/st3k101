from abc import abstractmethod
from typing import Dict, List, Union

from auth.roles import fulfills_role, Role
from auth.users import current_user
from framework.exceptions import BusinessRuleViolation
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingArg, TrackingType, translation_hybrid_updated, primitive_property_updated
from model.SQLAlchemy import db
from model.SQLAlchemy.models.OwnershipBase import OwnershipBase


__author__ = "Noah Hummel"


class SurveyBase(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'survey_base'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    reference_id = db.Column(db.String(128))
    _public = db.Column(db.Boolean, default=False)

    @property
    def public(self):
        return self._public

    @public.setter
    def public(self, value):
        if not fulfills_role(current_user(), Role.Contributor):
            raise BusinessRuleViolation('Only contributory may make items'
                                        'publicly available.')
        self._public = value

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        raise NotImplementedError

    @property
    @abstractmethod
    def tracker_args(self) -> Dict[str, List[Union[TrackingType, TrackingArg]]]:
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

        tracker_args = self.tracker_args[key]
        if TrackingType.Primitive in tracker_args:
            primitive_property_updated.send(
                self,
                key=key,
                previous_value=previous,
                new_value=value,
                person=current_user(),
                tracker_args=tracker_args
            )
        elif TrackingType.TranslationHybrid in tracker_args:
            translation_hybrid_updated.send(
                self,
                key=key,
                previous_value=previous,
                new_value=value,
                person=current_user(),
                tracker_args=tracker_args
            )

    def __init__(self, **kwargs):
        super(SurveyBase, self).__init__(**kwargs)
        self.owners.append(current_user())

    def accessible_by(self, party):
        return super(SurveyBase, self).accessible_by(party) or self.template

    def modifiable_by(self, party):
        return super(SurveyBase, self).accessible_by(party)

    # TODO: add original_language
