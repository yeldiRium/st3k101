from flask import g

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionStatistic import QuestionStatistic


class QuestionGroup(DataObject):
    def add_new_question(self, text: str) -> Question:
        question = Question()
        question.i15d_text = I15dString()
        question.i15d_text.add_locale(g._current_user.locale, text)

        question_statistic = QuestionStatistic()
        question_statistic.question = question
        question.statistic = question_statistic
        self.questions.add(question)
        return question

    def remove_question(self, question: Question):
        try:
            self.questions.remove(question)
            question.remove()
        except KeyError as _:
            raise QuestionNotFoundException(self.name, question.text)

QuestionGroup.name = DataAttribute(QuestionGroup, "name")
QuestionGroup.color = DataAttribute(QuestionGroup, "color")
QuestionGroup.text_color = DataAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = DataPointerSet(QuestionGroup, "questions", Question)
