from typing import List


from model import db
from model.models.OwnershipBase import OwnershipBase
from model.models.QuestionResponse import QuestionResponse

__author__ = "Noah Hummel, Hannes Leutloff"


class QuestionStatistic(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # columns
    smallest = db.Column(db.SmallInteger, nullable=False, default=0)
    biggest = db.Column(db.SmallInteger, nullable=False, default=0)
    q1 = db.Column(db.Float, nullable=False, default=0)
    q2 = db.Column(db.Float, nullable=False, default=0)
    q3 = db.Column(db.Float, nullable=False, default=0)
    n = db.Column(db.BigInteger, nullable=False, default=0)

    # foreign keys
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship(
        'Question',
        back_populates='statistic',
        foreign_keys=[question_id]
    )

    @staticmethod
    def calculate_median(values: List[QuestionResponse]) -> float:
        """
        Returns the median value of all QuestionResults
        """
        list.sort(values, key=lambda x: x.value)
        n = len(values)

        if n == 0:
            return 0

        n_half = n // 2
        if n % 2 == 0:
            return (values[n_half - 1].value + values[n_half].value) // 2
        else:
            return int(values[n_half].value)

    def update(self):
        """
        Updates the statistics taking into account all QuestionResults of
        self.question that are verified.
        """
        results = QuestionResponse.query\
                                  .filter_by(question_id=self.question_id,
                                             verified=True)\
                                  .order_by(QuestionResponse.value).all()
        self.smallest = self.question.range_end
        self.biggest = self.question.range_start

        for result in results:
            if result.value < self.smallest:
                self.smallest = result.value
            if result.value > self.biggest:
                self.biggest = result.value

        self.n = n = len(results)

        self.q2 = self.calculate_median(results)
        if n % 2 == 0:
            self.q1 = self.calculate_median(results[:n // 2])
            self.q3 = self.calculate_median(results[n // 2:])

        if n % 4 == 1:
            if n == 1:
                self.q1 = int(results[0].value)
                self.q3 = int(results[0].value)
            else:
                n_hat = n // 4
                self.q1 = 0.25 * int(
                    results[n_hat - 1].value) + 0.75 * int(
                    results[n_hat].value)
                self.q3 = 0.75 * int(
                    results[3 * n_hat].value) + 0.25 * int(
                    results[3 * n_hat + 1].value)
        if n % 4 == 3:
            n_hat = n // 4
            self.q1 = 0.25 * int(results[n_hat].value) + 0.75 * int(
                results[n_hat + 1].value)
            self.q3 = 0.75 * int(
                results[3 * n_hat + 1].value) + 0.25 * int(
                results[3 * n_hat + 2].value)
