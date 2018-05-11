from typing import List

from deprecated import deprecated

from model.SQLAlchemy import db
from model.SQLAlchemy.models.QuestionResult import QuestionResult

__author__ = "Noah Hummel, Hannes Leutloff"


class QuestionStatistic(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    smallest = db.Column(db.SmallInteger, nullable=False, default=0)
    biggest = db.Column(db.SmallInteger, nullable=False, default=0)
    q1 = db.Column(db.Float, nullable=False, default=0)
    q2 = db.Column(db.Float, nullable=False, default=0)
    q3 = db.Column(db.Float, nullable=False, default=0)
    n = db.Column(db.BigInteger, nullable=False, default=0)

    # foreign keys
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "n"')
    def answer_count(self) -> int:
        return self.n

    @answer_count.setter
    @deprecated(version='2.0', reason='Attribute has been renamed to "n"')
    def answer_count(self, n: int):
        self.n = n

    @staticmethod
    def median(values: List[QuestionResult]) -> float:
        """
        Returns the median value of all QuestionResults
        """
        list.sort(values, key=lambda x: x.answer_value)
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
        results = QuestionResult.query\
                                .filter_by(question=self.question, verified=True)\
                                .order_by(QuestionResult.value).all()
        self.smallest = None
        self.biggest = None

        for result in results:
            if self.smallest is None or result.value < self.smallest:
                self.smallest = result.value
            if self.biggest is None or result.value > self.biggest:
                self.biggest = result.value

        self.n = n = len(results)

        self.q2 = self.median(results)
        if n % 2 == 0:
            self.q1 = self.median(results[:n // 2])
            self.q3 = self.median(results[n // 2:])

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
