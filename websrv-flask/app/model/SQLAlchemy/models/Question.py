from typing import List

from sqlalchemy.dialects.postgresql import HSTORE

from model.SQLAlchemy import db, translation_hybrid
from model.SQLAlchemy.models.DataSubject import DataSubject
from model.SQLAlchemy.models.QuestionResult import QuestionResult

from deprecated import deprecated

from model.SQLAlchemy.models.QuestionStatistic import QuestionStatistic

__author__ = "Noah Hummel"


class Question(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    range = db.Column(db.SmallInteger, default=10, nullable=False)
    dirty = db.Column(db.Boolean, default=False, nullable=False)

    # translatable columns
    text_translations = db.Column(HSTORE)
    text = translation_hybrid(text_translations)

    # relationships
    results = db.relationship('QuestionResult', backref='question', lazy=True,
                              cascade='all, delete-orphan')
    statistic = db.relationship('QuestionStatistic', uselist=False,
                                backref='question',
                                cascade='all, delete-orphan')

    # foreign keys
    question_group_id = db.Column(db.Integer,
                                  db.ForeignKey('question_group.id'))

    def __init__(self, text: str, **kwargs):
        super(Question, self).__init__(text=text, **kwargs)
        self.statistic = QuestionStatistic()

    @staticmethod
    @deprecated(version='2.0', reason='Use Question() constructor directly')
    def create_question(text: str) -> 'Question':
        """
        Factory method to create a Question with default values and an asso-
        ciated statistics object.
        :param text: The text for the new question
        :return: The newly created Question instance
        """

        return Question(text=text)

    @deprecated(version='2.0', reason='Is implemented by database cascades.'
                                      'Use Question.results.remove(result) instead.')
    def remove_question_result(self, question_result: QuestionResult):
        """
        Removes a QuestionResult from this Question and the database.
        :param question_result: The result to remove
        """
        self.results.remove(question_result)

    @deprecated(version='2.0', reason='Use Question.text attribute directly.')
    def update_text(self, text: str):
        self.text = text

    def get_results_by_subject(self, subject: DataSubject) \
            -> List[QuestionResult]:
        query = QuestionResult.query.filter_by(data_subject=subject,
                                               question=self)
        return query.all()

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
