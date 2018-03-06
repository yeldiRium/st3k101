from flask import g

from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from model.I15dString import I15dString
from model.QuestionResult import QuestionResult
from model.QuestionStatistic import QuestionStatistic


class Question(DataObject):

    readable_by_anonymous = True

    @staticmethod
    def create_question(text: str):
        question = Question()
        question.text = I15dString()
        question.text.set_locale(text, g._locale)

        question_statistic = QuestionStatistic()
        question_statistic.question = question
        question.statistic = question_statistic

        return question

    def add_question_result(self, question_result: QuestionResult):
        self.results.add(question_result)


# These are here to prevent circular dependencies in QuestionStatistic and
# QuestionResult modules
QuestionStatistic.question = DataPointer(QuestionStatistic, "question",
                                         Question)
QuestionResult.question = DataPointer(QuestionResult, "question", Question)
Question.text = DataPointer(Question, "text", I15dString)
Question.statistic = DataPointer(Question, "statistic", QuestionStatistic,
                                 cascading_delete=True, serialize=False)
Question.results = DataPointerSet(Question, "results", QuestionResult,
                                  cascading_delete=True, serialize=False)
