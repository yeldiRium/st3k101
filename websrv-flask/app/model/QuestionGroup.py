import re

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString
from model.Question import Question


def check_color(color: str):
    regex = re.compile(r'^#[0-9a-fA-F]{6}$')
    if regex.match(color) is None:
        raise ValueError("'{}' is not a well formatted color value. It must be "
                         "a hex-string beginning with #.".format(color))


class QuestionGroup(DataObject):
    readable_by_anonymous = True

    @staticmethod
    def create_question_group(name: str):
        question_group = QuestionGroup()
        question_group.name = I15dString()
        question_group.name.set_locale(name)
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
            raise QuestionNotFoundException(self.name.get_default_text(),
                                            question.text.get_default_text())

    def set_name(self, name):
        self.name.set_locale(name)

    def set_color(self, color):
        check_color(color)
        self.color = color

    def set_background_color(self, text_color):
        check_color(text_color)
        self.text_color = text_color


QuestionGroup.name = DataPointer(QuestionGroup, "name", I15dString)
QuestionGroup.color = DataAttribute(QuestionGroup, "color")
QuestionGroup.text_color = DataAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = DataPointerSet(QuestionGroup, "questions", Question)
