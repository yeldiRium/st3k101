from abc import abstractmethod
from typing import Dict

from model.SQLAlchemy.v2_models.DataSubject import DataSubject
from model.SQLAlchemy.v2_models.QuestionResult import QuestionResult
from model.SQLAlchemy.v2_models.QuestionStatistic import QuestionStatistic
from model.SQLAlchemy.v2_models.SurveyBase import SurveyBase
from model.SQLAlchemy import db, MUTABLE_HSTORE, translation_hybrid

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
    results = db.relationship(
        'QuestionResult',
        backref='question',
        lazy=True,
        cascade='all, delete-orphan',
        foreign_keys=['question_result.id']
    )
    statistic = db.relationship(
        'QuestionStatistic',
        uselist=False,
        backref='question',
        cascade='all, delete-orphan',
        foreign_keys=[statistic_id]
    )

    def __init__(self, text: str, **kwargs):
        super(Question, self).__init__(text=text, **kwargs)
        self.statistic = QuestionStatistic()

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

    @staticmethod
    def get_results_by_subject(subject: DataSubject):
        results = QuestionResult.query.filter(
            QuestionResult.owners.any(id=subject.id)
        ).all()
        return results

    def add_question_result(self, answer_value: int, subject_email: str,
                            needs_verification: bool=True,
                            verification_token: str="") -> bool:
        """
        Adds a new QuestionResult to the Question.
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

        result = QuestionResult(question=self, data_subject=subject,
                                value=answer_value,
                                verified=(not needs_verification),
                                verification_token=verification_token)
        self.results.append(result)

        # replacement business logic for previous results
        if len(earlier_results) == 0:
            return True

        elif len(earlier_results) == 1:
            earlier_result = earlier_results[0]
            # replace earlier unverified result, or earlier verified
            # result, if new result is already verified
            if not earlier_result.verified or result.verified:
                self.results.remove(earlier_result)

        elif len(earlier_results) == 2:
            verified_result = verified_results[0]
            unverified_result = unverified_results[0]
            # cancel pending unverified result
            self.results.remove(unverified_result)
            if result.verified:
                # replace earlier result
                self.results.remove(verified_result)

        # TODO: not necessary anymore because answer count is selected on the fly
        return False  # signal that answer count has not changed


class ConcreteQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)

    __tablename__ = 'concrete_question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    range = db.Column(db.SmallInteger, default=10, nullable=False)

    # translatable columns
    text_translations = db.Column(MUTABLE_HSTORE)
    text = translation_hybrid(text_translations)


class ShadowQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)

    __tablename__ = 'shadow_question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteQuestion.id))
    _referenced_object = db.relationship(ConcreteQuestion,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    @property
    def text(self) -> str:
        return self._referenced_object.text

    @property
    def text_translations(self) -> Dict[str, str]:
        return self._referenced_object.text_translations

    @property
    def range(self) -> int:
        return self._referenced_object.range
