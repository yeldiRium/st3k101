import os
from abc import abstractmethod
from typing import Dict, List

import utils
from auth.users import current_user
from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType, translation_hybrid_updated, property_updated
from model import db
from model.models.OwnershipBase import OwnershipBase


__author__ = "Noah Hummel"


class SurveyBase(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # SQLA polymorphic config
    __tablename__ = 'survey_base'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # SQLA columns
    _template = db.Column(db.Boolean, default=False)
    _reference_id = db.Column(db.String(128))

    @property
    def template(self) -> bool:
        """
        :return: Whether self may be used as a template.
        """
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def reference_id(self) -> str:
        # set initial reference_id if name already present
        if not self._reference_id:
            if self.name is not None and len(self.name) > 0:
                self._reference_id = self.generate_reference_id()
        return self._reference_id

    @reference_id.setter
    def reference_id(self, value: str):
        self._reference_id = utils.unicode_to_xml_friendly_ascii(value)

    @property
    def available_languages(self):
        return [BabelLanguage[k] for k in self.name_translations.keys()]

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        """
        :return: The original BabelLanguage self was created in.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def shadow(self) -> bool:
        """
        :return: Whether self is a shadow instance.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def tracker_args(self) -> Dict[str, TrackingType]:
        """
        A dictionary containing information on properties whose changes should
        be tracked.
        Hint: tracker_args should be defined as a class-attribute.

        The format is as follows:

        tracker_entries = {
            __("attribute_name"): TrackingType
        }

        It is not required to wrap the attribute_name with "__()", but doing so
        will mark the attribute_name to be added to the translation catalogues.
        If translations are provided, the attribute_name will be translated
        automatically.
        :return: A dictionary containing information on properties whose changes
        should be tracked.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """
        :return: A human readable name for self in the current request's
        BabelLanguage
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name_translations(self) -> Dict[str, str]:
        """
        :return: A dictionary containing all translations of self's human
        readable name
        """
        raise NotImplementedError

    def __setattr__(self, key, value):
        """
        Hook for activity tracking, see tracker_args for more information.
        """

        if key not in self.tracker_args.keys():
            object.__setattr__(self, key, value)  # just set attribute
            return

        if hasattr(self, key):
            previous = getattr(self, key)
        else:
            previous = None
        object.__setattr__(self, key, value)

        key = _(key)  # translate property name if possible

        signal = None  # decide on appropriate signal type
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

    def accessible_by(self, party: "Party") -> bool:
        """
        Checks if party may access (read from) self.
        :param party: The Party in question.
        :return: Whether the Party may read from self.
        """
        return super(SurveyBase, self).accessible_by(party) or self.template

    def modifiable_by(self, party: "Party") -> bool:
        """
        Checks if party may modify (write to) self.
        :param party: The party in question.
        :return: Whether the Party may write to self.
        """
        return super(SurveyBase, self).accessible_by(party)

    def generate_reference_id(self) -> str:
        while True:
            name = self.name_translations[self.original_language.name]
            name_sane = utils.unicode_to_xml_friendly_ascii(name)
            if len(name_sane) > 15:
                name_sane = name_sane[:15]
            random_chars = os.urandom(5).hex()
            reference_id = (name_sane + "-" + random_chars).replace(" ", "-")

            # check if reference_id is unique
            others = SurveyBase.query.filter_by(_reference_id=reference_id).all()
            if not others:
                break

        return reference_id
