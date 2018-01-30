from flask import g

from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from model.I15dString import I15dString
from model.QuestionResult import QuestionResult
from model.QuestionStatistic import QuestionStatistic


class Question(DataObject):
    exposed_properties = {
        "text"
    }

    @staticmethod
    def create_question(text: str):
        question = Question()
        question.i15d_text = I15dString()
        question.text = text

        question_statistic = QuestionStatistic()
        question_statistic.question = question
        question.statistic = question_statistic

        return question

    def add_question_result(self, question_result: QuestionResult):
        self.results.add(question_result)

    @property
    def text(self):
        return self.i15d_text.get()

    @text.setter
    def text(self, text: str):
        self.i15d_text.add_locale(g._locale, text)


# These are here to prevent circular dependencies in QuestionStatistic and
# QuestionResult modules
QuestionStatistic.question = DataPointer(QuestionStatistic, "question",
                                         Question)
QuestionResult.question = DataPointer(QuestionResult, "question", Question)
Question.i15d_text = DataPointer(Question, "i15d_text", I15dString,
                                 serialize=False)
Question.statistic = DataPointer(Question, "statistic", QuestionStatistic,
                                 cascading_delete=True)
Question.results = DataPointerSet(Question, "results", QuestionResult,
                                  cascading_delete=True)
