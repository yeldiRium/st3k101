from model.SQLAlchemy import db

from deprecated import deprecated

__author__ = "Noah Hummel"


class QuestionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.SmallInteger, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(32))

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    data_subject_id = db.Column(db.Integer, db.ForeignKey('data_subject.id'))

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "value"')
    def answer_value(self) -> int:
        return self.value

    @staticmethod
    @deprecated(version='2.0', reason='Use QuestionResult() constructor directly')
    def new(question, data_subject, value: int,
            needs_verification: bool, verification_token: str) \
            -> 'QuestionResult':
        """
        Factory method for creating a new QuestionResult instance
        :type question: Question
        :type data_subject: DataSubject
        :param question: The question that was answered
        :param data_subject: The subject who answered the question
        :param value: The value of the subject's answer
        :param needs_verification: Whether the result needs email verification
        :param verification_token: The email verification token
        :return: The newly created QuestionResult instance
        """
        result = QuestionResult(question=question, data_subject=data_subject,
                                value=value, verified=(not needs_verification),
                                verification_token=verification_token)
        return result

    def verify(self) -> bool:
        """
        Used to verify a QuestionResult to make it count into the statistic.
        :return: bool Indicating whether the answer count for the corresponding
        question increased
        """
        question = self.question

        earlier_results = question.get_results_by_subject(self.data_subject)
        verified_results = list(filter(lambda x: x.verified, earlier_results))

        for vr in verified_results:  # remove previous verified result(s?)
            question.remove_question_result(vr)

        self.verified = True

        return len(verified_results) == 0  # no previous verified results?
