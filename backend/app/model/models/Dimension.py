from abc import abstractmethod
from typing import Dict

from flask import g

from framework.exceptions import BusinessRuleViolation
from framework.internationalization import __
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType
from framework.signals import item_added, item_removed
from model import db, MUTABLE_HSTORE, translation_hybrid
from model.models.Question import Question, ConcreteQuestion, ShadowQuestion
from model.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


class Dimension(SurveyBase):
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    randomize_question_order = db.Column(db.Boolean, nullable=False,
                                         default=False)

    # foreign keys
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))

    # relationships
    questions = db.relationship(
        'Question',
        backref='dimension',
        cascade='all, delete-orphan',
        foreign_keys=[Question.dimension_id]
    )

    tracker_args = {
        __('name'): TrackingType.TranslationHybrid,
        __('randomize_question_order'): TrackingType.Primitive
    }

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
    def shadow(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        raise NotImplementedError

    def new_question(self, text: str, **kwargs) -> ConcreteQuestion:
        if not isinstance(self, ConcreteDimension):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        question = ConcreteQuestion(text, **kwargs)
        self.questions.append(question)

        item_added.send(self, added_item=question)

        return question

    def add_shadow_question(self, concrete_question: ConcreteQuestion)\
            -> ShadowQuestion:
        if not isinstance(self, ConcreteDimension):
            raise BusinessRuleViolation("Can't modify shadow instances!")

        question = ShadowQuestion(concrete_question)
        self.questions.append(question)

        item_added.send(self, added_item=question)

        return question

    def remove_question(self, question):
        if not isinstance(self, ConcreteDimension):
            raise BusinessRuleViolation("Can't modify shadow instances!")
        if question not in self.questions:
            raise KeyError("Question not in Dimension.")

        copies = []
        if question.shadow:
            for dimension_copy in self.copies:
                copies += list(filter(
                    lambda q: q.concrete_id == question.concrete_id if q.shadow else False,
                    dimension_copy.questions
                ))
        else:
            copies = question.copies
        for copy in copies:
            db.session.delete(copy)

        item_removed.send(self, removed_item_name=question.text)

        self.questions.remove(question)


class ConcreteDimension(Dimension):
    id = db.Column(db.Integer, db.ForeignKey(Dimension.id), primary_key=True)

    __tablename__ = 'concrete_dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)

    shadow = False

    def __init__(self, name: str, **kwargs):
        self.original_language = g._language
        super(ConcreteDimension, self).__init__(name=name, **kwargs)
        self.reference_id = SurveyBase.generate_reference_id(self)

    @staticmethod
    def from_shadow(shadow):
        d = ConcreteDimension("")
        d.name_translations = shadow.name_translations
        d.original_language = shadow.original_language
        d.randomize_question_order = shadow.randomize_question_order
        d.owners = shadow.owners
        d.reference_id = shadow.reference_id

        for s_question in shadow.questions:
            c_question = ConcreteQuestion.from_shadow(s_question)
            d.questions.append(c_question)

        return d


class ShadowDimension(Dimension):
    id = db.Column(db.Integer, db.ForeignKey(Dimension.id), primary_key=True)

    __tablename__ = 'shadow_dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteDimension.id))
    _referenced_object = db.relationship(ConcreteDimension,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    shadow = True

    def __init__(self, dimension, **kwargs):
        self._referenced_object = dimension
        super(ShadowDimension, self).__init__(**kwargs)

        for question in dimension.questions:
            if not isinstance(question, ConcreteQuestion):
                question = question.concrete
            s_question = ShadowQuestion(question)
            self.questions.append(s_question)

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
    def original_language(self) -> BabelLanguage:
        return self._referenced_object.original_language

    @property
    def name(self) -> str:
        return self._referenced_object.name

    @property
    def name_translations(self) -> Dict[str, str]:
        return self._referenced_object.name_translations
