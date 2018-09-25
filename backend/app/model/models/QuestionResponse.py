from auth.session import current_user
from framework.signals import SIG_ANSWER_VOIDED, SIG_ANSWER_SUBMITTED
from model import db
from model.models.DataSubject import DataSubject
from model.models.OwnershipBase import OwnershipBase

__author__ = "Noah Hummel"


class QuestionResponse(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)
    value = db.Column(db.SmallInteger, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(32))
    xapi_statement = db.Column(db.JSON)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __init__(self, data_subject: DataSubject=None, **kwargs):
        super(QuestionResponse, self).__init__(**kwargs)
        if data_subject is not None:
            self.owners.append(data_subject)
        self.owners += self.question.owners

    def verify(self) -> bool:
        """
        Used to verify a QuestionResponse to make it count into the statistic.
        :return: bool Indicating whether the answer count for the corresponding
        question increased
        """
        question = self.question

        earlier_results = question.get_results_by_subject(self.data_subject)
        verified_results = list(filter(lambda x: x.verified, earlier_results))

        for vr in verified_results:  # remove previous verified result(s?)
            SIG_ANSWER_VOIDED.send(vr)
            question.remove_question_result(vr)

        self.verified = True
        self.verification_token = None
        SIG_ANSWER_SUBMITTED.send(self)

        return len(verified_results) == 0  # no previous verified results?
