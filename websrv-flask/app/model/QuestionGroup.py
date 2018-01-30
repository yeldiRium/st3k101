from flask import g

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionStatistic import QuestionStatistic


class QuestionGroup(DataObject):
    exposed_properties = {
        "name"
    }

    @staticmethod
    def create_question_group(name: str):
        question_group = QuestionGroup()
        question_group.i15d_name = I15dString()
        question_group.name = name
        question_group.color = "#FFFFFF"
        question_group.text_color = "#000000"
        question_group.questions = []
        return question_group

    def add_new_question(self, text: str) -> Question:
        question = Question.create_question(text)
        self.questions.add(question)
        return question

    def remove_question(self, question: Question):
        try:
            self.questions.remove(question)
            question.remove()
        except KeyError as _:
            raise QuestionNotFoundException(self.name, question.text)

    @property
    def name(self):
        return self.i15d_name.get()

    @name.setter
    def name(self, name: str):
        self.i15d_name.add_locale(g._locale, name)


QuestionGroup.i15d_name = DataPointer(QuestionGroup, "name", I15dString,
                                      serialize=False)
QuestionGroup.color = DataAttribute(QuestionGroup, "color")
QuestionGroup.text_color = DataAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = DataPointerSet(QuestionGroup, "questions", Question)
