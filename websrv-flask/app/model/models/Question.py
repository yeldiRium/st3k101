from abc import abstractmethod
from typing import Dict

from flask import g

from framework.internationalization import __
from framework.internationalization.babel_languages import BabelLanguage
from framework.tracker import TrackingType, TrackingArg
from model.models.DataSubject import DataSubject
from model.models.QuestionResponse import QuestionResponse
from model.models.QuestionStatistic import QuestionStatistic
from model.models.SurveyBase import SurveyBase
from model import db, MUTABLE_HSTORE, translation_hybrid

__author__ = "Noah Hummel"


class Question(SurveyBase):
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    dirty = db.Column(db.Boolean, default=False, nullable=False)

    # foreign keys
    dimension_id = db.Column(db.Integer, db.ForeignKey('dimension.id'))
    statistic_id = db.Column(db.Integer, db.ForeignKey('question_statistic.id'))

    # relationships
    responses = db.relationship(
        'QuestionResponse',
        backref='question',
        lazy=True,
        cascade='all, delete-orphan',
        foreign_keys=[QuestionResponse.question_id]
    )
    statistic = db.relationship(
        'QuestionStatistic',
        uselist=False,
        backref='question',
        cascade='all, delete-orphan',
        foreign_keys=[statistic_id],
        single_parent=True
    )

    tracker_args = {
        __('text'): [
            TrackingType.TranslationHybrid,
            TrackingArg.Accumulate
        ],
        __('range'): [
            TrackingType.Primitive
        ],
    }

    def __init__(self, **kwargs):
        super(Question, self).__init__(**kwargs)
        self.statistic = QuestionStatistic()

    @property
    @abstractmethod
    def reference_id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def text(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def text_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def range(self) -> int:
        raise NotImplementedError

    @property
    def original_language(self) -> str:
        return self.dimension.original_language

    @property
    def available_languages(self):
        return [BabelLanguage[k] for k in self.text_translations.keys()]

    @staticmethod
    def get_results_by_subject(subject: DataSubject):
        results = QuestionResponse.query.filter(
            QuestionResponse.owners.any(id=subject.id)
        ).all()
        return results

    def add_question_result(self, answer_value: int, subject_email: str,
                            needs_verification: bool=True,
                            verification_token: str="") -> bool:
        """
        Adds a new QuestionResponse to the Question.
        :param answer_value: int The value the DataSubject has chosen
        :param subject_email: str The email address of the DataSubject
        :param needs_verification: bool Indicating whether this result need to
                                        be verified
        :param verification_token: str The verification token to be used when
                                       verifying the result
        :return: bool Indicating whether the answer count has increased or not
        """
        self.dirty = True  # FIXME: might not actually be dirty yet

        subject = DataSubject.get_or_create(subject_email)
        earlier_results = self.get_results_by_subject(subject)
        verified_results = list(filter(lambda x: x.verified, earlier_results))
        unverified_results = list(filter(lambda x: not x.verified,
                                         earlier_results))

        result = QuestionResponse(question=self, data_subject=subject,
                                  value=answer_value,
                                  verified=(not needs_verification),
                                  verification_token=verification_token)
        self.responses.append(result)

        # replacement business logic for previous results
        if len(earlier_results) == 0:
            return True

        elif len(earlier_results) == 1:
            earlier_result = earlier_results[0]
            # replace earlier unverified result, or earlier verified
            # result, if new result is already verified
            if not earlier_result.verified or result.verified:
                self.responses.remove(earlier_result)

        elif len(earlier_results) == 2:
            verified_result = verified_results[0]
            unverified_result = unverified_results[0]
            # cancel pending unverified result
            self.responses.remove(unverified_result)
            if result.verified:
                # replace earlier result
                self.responses.remove(verified_result)

        # TODO: not necessary anymore because answer count is selected on the fly
        return False  # signal that answer count has not changed


class ConcreteQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)

    __tablename__ = 'concrete_question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    reference_id = db.Column(db.String(128))
    range_start = db.Column(db.SmallInteger, default=0, nullable=False)
    range_end = db.Column(db.SmallInteger, default=10, nullable=False)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)

    # translatable columns
    text_translations = db.Column(MUTABLE_HSTORE)
    text = translation_hybrid(text_translations)

    shadow = False

    def __init__(self, text: str, **kwargs):
        self.original_language = g._language
        super(ConcreteQuestion, self).__init__(text=text, **kwargs)

    @staticmethod
    def from_shadow(shadow):
        q = ConcreteQuestion("")
        q.dirty = shadow.dirty
        q.reference_id = shadow.reference_id

        stat = shadow.statistic
        shadow.statistic = None
        q.statistic = stat

        q.responses = shadow.results
        q.text_translations = shadow.text_translations
        q.owners = shadow.owners

        return q


class ShadowQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)

    __tablename__ = 'shadow_question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteQuestion.id))
    _referenced_object = db.relationship(ConcreteQuestion,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    shadow = True

    def __init__(self, question, **kwargs):
        super(ShadowQuestion, self).__init__(**kwargs)
        self._referenced_object = question

    @property
    def concrete_id(self):
        return self._referenced_object.id

    @property
    def concrete(self):
        return self._referenced_object

    @property
    def reference_id(self):
        return self._referenced_object.reference_id

    @property
    def text(self) -> str:
        return self._referenced_object.text

    @property
    def text_translations(self) -> Dict[str, str]:
        return self._referenced_object.text_translations

    @property
    def range_start(self) -> int:
        return self._referenced_object.range_start

    @property
    def range_end(self) -> int:
        return self._referenced_object.range_end
