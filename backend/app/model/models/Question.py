from abc import abstractmethod
from typing import Dict, List

from flask import g

from framework.internationalization import __
from framework.internationalization.babel_languages import BabelLanguage
from framework.signals import SIG_QUESTION_ANSWERED
from framework.tracker import TrackingType
from model.models.DataSubject import DataSubject
from model.models.OwnershipBase import query_owned
from model.models.QuestionResponse import QuestionResponse
from model.models.QuestionStatistic import QuestionStatistic
from model.models.SurveyBase import SurveyBase
from model import db, MUTABLE_HSTORE, translation_hybrid

__author__ = "Noah Hummel"


class Question(SurveyBase):
    """
    Base class for Shadow- and ConcreteQuestions.
    Not to be instantiated directly, use ConcreteQuestion to create a new
    Question, or ShadowQuestion to create a copy of a ConcreteQuestion.
    """
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    position = db.Column(db.Integer)

    # foreign keys
    dimension_id = db.Column(db.Integer, db.ForeignKey('dimension.id'))

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
        back_populates='question',
        cascade='all, delete-orphan',
        foreign_keys=[QuestionStatistic.question_id],
        single_parent=True
    )

    tracker_args = {
        __('text'): TrackingType.TranslationHybrid,
        __('range_start'): TrackingType.Primitive,
        __('range_end'): TrackingType.Primitive,
        __('range_start_label'): TrackingType.TranslationHybrid,
        __('range_end_label'): TrackingType.TranslationHybrid
    }

    def __init__(self, **kwargs):
        super(Question, self).__init__(**kwargs)
        self.statistic = QuestionStatistic()

    @property
    def name(self) -> str:
        """
        Inherited from SurveyBase.
        A name for this Question. For Questions, this is the same as Question.text.

        This property is internationalized, translations are stored in
        Question.name_translations.
        :return: str
        """
        return self.text

    @property
    def name_translations(self) -> Dict[str, str]:
        """
        Inherited from SurveyBase.
        All translations of Question.name. This is the same as Question.text_translations.

        Translations are stored as
            {
                "de": "Eine deutsche Übersetzung.",
                "en": "An english translation."
            }
        For available languages, see framework/internationalization/babel_languages
        :return: Dict[str, str]
        """
        return self.text_translations

    @property
    @abstractmethod
    def shadow(self) -> bool:
        """
        Inherited from SurveyBase.
        Whether self is a Shadow instance. If this is false, self is a Concrete instance.
        :return: bool
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def text(self) -> str:
        """
        The Question text.

        This property is internationalized, translations are stored in
        Question.text_translations.
        :return:
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def text_translations(self) -> Dict[str, str]:
        """
        All translations of Question.text.

        Translations are stored as
            {
                "de": "Eine deutsche Übersetzung.",
                "en": "An english translation."
            }
        For available languages, see framework/internationalization/babel_languages
        :return: Dict[str, str]
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_start_label(self) -> str:
        """
        The label for Question.range_start.

        This property is internationalized, translations are stored in
        Question.range_start_label_translations.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_start_label_translations(self) -> Dict[str, str]:
        """
        All translations of Question.range_start_label.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_end_label(self) -> str:
        """
        The label for Question.range_end.

        This property is internationalized, translations are stored in
        Question.range_end_label_translations.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_end_label_translations(self) -> Dict[str, str]:
        """
        All translations of Question.range_end_label.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_start(self) -> int:
        """
        The lower bound of the answer scale.

        range_start must always be lesser than range_end.
        :return: int
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def range_end(self) -> int:
        """
        The upper bound of the answer scale.

        range_end must always be greater than range_start.
        :return: int
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def original_language(self) -> BabelLanguage:
        """
        The language self was originally created in.
        Whenever a non-available translation is requested, this language is used.
        :return: BabelLanguage
        """
        raise NotImplementedError

    def get_question_responses_by_subject(self, subject: DataSubject) -> List[QuestionResponse]:
        """
        Returns a list of all QuestionResponses for for this Question which were
        submitted by a specific DataSubject.
        :param subject: DataSubject
        :return: List[QuestionResponse]
        """
        query = query_owned(DataSubject, subject.id, QuestionResponse)
        return query.filter(QuestionResponse.question_id == self.id).all()

    def add_question_result(self, answer_value: int, data_subject: DataSubject,
                            needs_verification: bool=True,
                            verification_token: str="") -> QuestionResponse:
        """
        Adds a new QuestionResponse to the Question.
        :param answer_value: int The value the DataSubject has chosen
        :param data_subject: DataSubject The DataSubject who submitted
        :param needs_verification: bool Indicating whether this result need to
                                        be verified
        :param verification_token: str The verification token to be used when
                                       verifying the result
        :return: bool Indicating whether the answer count has increased or not
        """
        earlier_results = self.get_question_responses_by_subject(data_subject)
        verified_results = list(filter(lambda x: x.verified, earlier_results))
        unverified_results = list(filter(lambda x: not x.verified,
                                         earlier_results))

        result = QuestionResponse(question=self, data_subject=data_subject,
                                  value=answer_value,
                                  verified=(not needs_verification),
                                  verification_token=verification_token)
        self.responses.append(result)

        # replacement business logic for previous results
        if len(earlier_results) == 1:
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

        SIG_QUESTION_ANSWERED.send(result)
        return result


class ConcreteQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey(Question.id), primary_key=True)

    # sqla config
    __tablename__ = 'concrete_question'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    range_start = db.Column(db.SmallInteger, default=0, nullable=False)
    range_end = db.Column(db.SmallInteger, default=10, nullable=False)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)

    # translatable columns
    text_translations = db.Column(MUTABLE_HSTORE)
    text = translation_hybrid(text_translations)
    range_start_label_translations = db.Column(MUTABLE_HSTORE)
    range_start_label = translation_hybrid(range_start_label_translations)  # TODO: somehow include this in xAPI statement
    range_end_label_translations = db.Column(MUTABLE_HSTORE)
    range_end_label = translation_hybrid(range_end_label_translations)

    shadow = False

    def __init__(self, text: str, range_start_label: str, range_end_label: str, **kwargs):
        self.original_language = g._language
        super(ConcreteQuestion, self).__init__(
            text=text,
            range_start_label=range_start_label,
            range_end_label=range_end_label,
            **kwargs
        )
        self.reference_id = SurveyBase.generate_reference_id(self)

    @staticmethod
    # FIXME: confusing naming: this actually converts a shadow to a concrete,
    # the owner must be the same
    def from_shadow(shadow):
        """
        Factory method for ConcreteQuestion.
        Creates a new ConcreteQuestion with contents of given ShadowQuestion.

        This is used when a concrete instance is deleted, but there are shadows pointing to
        it. In this case, the shadow is converted to a concrete instance.
        :param shadow:
        """
        q = ConcreteQuestion("", "", "")
        q.dirty = shadow.dirty
        q.reference_id = shadow.reference_id
        q.original_language = shadow.original_language

        # TODO: This should actually clone the statistic object instead of re-assigning it
        # q.statistic = shadow.statistic.clone()
        stat = shadow.statistic
        shadow.statistic = None
        q.statistic = stat

        q.responses = shadow.responses
        q.text_translations = shadow.text_translations
        q.range_start_label_translations = shadow.range_start_label_translations
        q.range_end_label_translations = shadow.range_end_label_translations
        q.owners = shadow.owners
        q.range_start = shadow.range_start
        q.range_end = shadow.range_end

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
        self._referenced_object = question
        super(ShadowQuestion, self).__init__(**kwargs)

    @property
    def concrete_id(self):
        return self._referenced_object.id

    @property
    def concrete(self):
        return self._referenced_object

    @property
    def original_language(self) -> BabelLanguage:
        return self._referenced_object.original_language

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

    @property
    def range_start_label(self) -> str:
        return self._referenced_object.range_start_label

    @property
    def range_start_label_translations(self) -> Dict[str, str]:
        return self._referenced_object.range_start_label_translations

    @property
    def range_end_label(self) -> str:
        return self._referenced_object.range_end_label

    @property
    def range_end_label_translations(self) -> Dict[str, str]:
        return self._referenced_object.range_end_label_translations
