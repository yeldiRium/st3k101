from model.SQLAlchemy import db
from model.SQLAlchemy.v2_models.OwnershipBase import OwnershipBase

__author__ = "Noah Hummel"


class QuestionResult(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)
    value = db.Column(db.SmallInteger, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(32))

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

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
