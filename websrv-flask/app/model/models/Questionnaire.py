from abc import abstractmethod
from typing import Dict

from flask import g

from auth.users import current_user
from framework.exceptions import BusinessRuleViolation
from framework.internationalization import __
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType, item_added, item_removed, questionnaire_removed
from model import db, MUTABLE_HSTORE, translation_hybrid
from model.models.Dimension import Dimension, ConcreteDimension, ShadowDimension
from model.models.QuestionResponse import QuestionResponse
from model.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


class Questionnaire(SurveyBase):
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    published = db.Column(db.Boolean, nullable=False, default=False)
    allow_embedded = db.Column(db.Boolean, nullable=False, default=False)
    xapi_target = db.Column(db.String(512))

    # challenge data
    email_whitelist = db.Column(db.ARRAY(db.String))
    email_whitelist_enabled = db.Column(db.Boolean)
    email_blacklist = db.Column(db.ARRAY(db.String))
    email_blacklist_enabled = db.Column(db.Boolean)
    password = db.Column(db.String(64))
    password_enabled = db.Column(db.Boolean)

    # relationships
    dimensions = db.relationship(
        'Dimension',
        backref='questionnaire',
        cascade='all, delete-orphan',
        foreign_keys=[Dimension.questionnaire_id]
    )

    tracker_args = {
        __('name'): TrackingType.TranslationHybrid,
        __('description'): TrackingType.TranslationHybrid,
        __('password_enabled'): TrackingType.Primitive,
        __('password'): TrackingType.Primitive,
        __('email_blacklist'): TrackingType.Primitive,
        __('email_whitelist'): TrackingType.Primitive,
        __('email_blacklist_enabled'): TrackingType.Primitive,
        __('email_whitelist_enabled'): TrackingType.Primitive,
        __('published'): TrackingType.Primitive
    }

    def __init__(self, **kwargs):
        super(Questionnaire, self).__init__(**kwargs)
        self.password = ''
        self.email_blacklist = []
        self.email_whitelist = []
        self.password_enabled = False
        self.email_blacklist_enabled = False
        self.email_whitelist_enabled = False

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        raise NotImplementedError

    @property
    def available_languages(self):
        return [BabelLanguage[k] for k in self.name_translations.keys()]

    @property
    def question_count(self) -> int:
        """
        :return: The number of questions associated with the Questionnaire.
        """
        count = 0
        for dim in self.dimensions:
            count += len(dim.questions)
        return count

    @property
    def answer_count(self) -> int:
        """
        :return: The number of verified answers for the Questionnaire.
        """
        count = 0
        for qg in self.question_groups:
            for q in qg.questions:
                verified_results = QuestionResponse.query.\
                    filter_by(question=q, verified=True).all()
                count += len(verified_results)
        n_questions = self.question_count
        if n_questions < 1:
            n_questions = 1
        return count // n_questions

    def new_dimension(self, name: str) -> ConcreteDimension:
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        dimension = ConcreteDimension(name)
        self.dimensions.append(dimension)

        for copy in self.copies:
            s_dimension = ShadowDimension(dimension)
            s_dimension.owners = copy.owners
            copy.dimensions.append(s_dimension)

        item_added.send(self, added_item=dimension)

        return dimension

    def add_shadow_dimension(self, concrete_dimension: ConcreteDimension)\
            -> ShadowDimension:
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        dimension = ShadowDimension(concrete_dimension)
        self.dimensions.append(dimension)

        for copy in self.copies:
            s_dimension = ShadowDimension(concrete_dimension)
            s_dimension.owners = copy.owners
            copy.dimensions.append(s_dimension)

        item_added.send(added_item=dimension)

        return dimension

    def remove_dimension(self, dimension):
        if not isinstance(self, ConcreteQuestionnaire):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        if dimension not in self.dimensions:
            raise KeyError("Question not in Dimension.")
        for copy in [*self.copies, self]:
            for s_dimension in copy.dimensions:
                if not isinstance(s_dimension, ShadowDimension):
                    continue
                if s_dimension.concrete_id == dimension.id:
                    db.session.delete(s_dimension)

        item_removed.send(self, removed_item_name=dimension.name)

        self.dimensions.remove(dimension)

    def delete(self):

        questionnaire_removed.send(self)

        if isinstance(self, ConcreteQuestionnaire):
            # Create concrete questionnaires from all shadow copies of
            # this questionnaire. We don't want to deletes other peoples'
            # questionnaires.
            for copy in self.copies:
                q = ConcreteQuestionnaire.from_shadow(copy)
                db.session.add(q)
            for copy in self.copies:
                db.session.delete(copy)

        db.session.delete(self)


class ConcreteQuestionnaire(Questionnaire):
    id = db.Column(db.Integer, db.ForeignKey(Questionnaire.id), primary_key=True)

    __tablename__ = 'concrete_questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    reference_id = db.Column(db.String(128))
    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)
    description_translations = db.Column(MUTABLE_HSTORE)
    description = translation_hybrid(description_translations)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)

    shadow = False

    def __init__(self, name, description, **kwargs):
        self.original_language = g._language
        super(ConcreteQuestionnaire, self).__init__(name=name,
                                                    description=description,
                                                    **kwargs)

    @staticmethod
    def from_shadow(shadow):
        q = ConcreteQuestionnaire("", "")
        q.name_translations = shadow.name_translations
        q.description_translations = shadow.description_translations
        q.original_language = shadow.original_language
        q.published = shadow.published
        q.allow_embedded = shadow.allow_embedded
        q.xapi_target = shadow.xapi_target
        q.owners = shadow.owners
        q.reference_id = shadow.reference_id

        for s_dimension in shadow.dimensions:
            c_dimension = ConcreteDimension.from_shadow(s_dimension)
            q.dimensions.append(c_dimension)

        return q


class ShadowQuestionnaire(Questionnaire):
    id = db.Column(db.Integer, db.ForeignKey(Questionnaire.id), primary_key=True)

    __tablename__ = 'shadow_questionnaire'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteQuestionnaire.id))
    _referenced_object = db.relationship(ConcreteQuestionnaire,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    shadow = True

    def __init__(self, questionnaire, **kwargs):
        super(ShadowQuestionnaire, self).__init__(**kwargs)
        self._referenced_object = questionnaire

        for dimension in questionnaire.dimensions:
            if not isinstance(dimension, ConcreteDimension):
                dimension = dimension.concrete
            s_dimension = ShadowDimension(dimension)
            self.dimensions.append(s_dimension)

    @property
    def concrete_id(self):
        if self._referenced_object is None:
            return None
        return self._referenced_object.id

    @property
    def concrete(self):
        if self._referenced_object is None:
            return None
        return self._referenced_object

    @property
    def reference_id(self):
        return self._referenced_object.reference_id

    @property
    def name(self) -> str:
        return self._referenced_object.name

    @property
    def name_translations(self) -> Dict[str, str]:
        return self._referenced_object.name_translations

    @property
    def description(self) -> str:
        return self._referenced_object.description

    @property
    def description_translations(self) -> Dict[str, str]:
        return self._referenced_object.description_translations

    @property
    def original_language(self) -> BabelLanguage:
        return self._referenced_object.original_language
