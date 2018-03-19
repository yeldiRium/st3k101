import re

from flask import g

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString
from model.Question import Question

__author__ = "Noah Hummel, Hannes Leutloff"


def check_color(color: str) -> None:
    """
    A helper function to check the validity of hex color codes. Raises
    ValueError if color format is invalid.
    :param color: str The hex color code to check
    :return: None
    """
    regex = re.compile(r'^#[0-9a-fA-F]{6}$')
    if regex.match(color) is None:
        raise ValueError("'{}' is not a well formatted color value. It must be "
                         "a hex-string beginning with #.".format(color))


class QuestionGroup(DataObject):
    """
    A DataObject representing a group of Question to be displayed together
    in a Questionnaire.
    """

    readable_by_anonymous = True

    @staticmethod
    def create_question_group(name: str) -> "QuestionGroup":
        """
        Factory method to create a new QuestionGroup with default values
        :param name: str The name of the new Question
        :return: QuestionGroup The newly created QuestionGroup
        """
        question_group = QuestionGroup()
        question_group.name = I15dString.new(name)
        question_group.color = g._config["QUESTIONGROUP_DEFAULT_COLOR"]
        question_group.text_color = g._config["QUESTIONGROUP_DEFAULT_TEXTCOLOR"]
        question_group.questions = []
        return question_group

    def add_new_question(self, text: str) -> Question:
        """
        Adds a new question to the QuestionGroup.
        :param text: str The Question text of the new Question
        :return: Question The newly created Question
        """
        question = Question.create_question(text)
        self.questions.add(question)
        return question

    def remove_question(self, question: Question) -> None:
        """
        Removes a Question from the QuestionGroup.
        :param question: Question The question to remove
        :return: None
        """
        try:
            self.questions.remove(question)
            question.remove()
        except KeyError as _:
            raise QuestionNotFoundException(self.name.get_default_text(),
                                            question.text.get_default_text())

    def set_name(self, name: str) -> None:
        """
        Setter for QuestionGroup.name, wraps setter of I15dString
        :param name: str The new name of the QuestionGroup
        :return: None
        """
        self.name.set_locale(name)

    def set_color(self, color: str) -> None:
        """
        Setter for QuestionGroup.color, checks if color is valid
        :param color: str A html hex color code
        :return: None
        """
        check_color(color)
        self.color = color

    def set_background_color(self, text_color: str) -> None:
        """
        Setter for QuestionGroup.text_color, checks if color is valid
        :param text_color: str A html hex color code
        :return: None
        """
        check_color(text_color)
        self.text_color = text_color


QuestionGroup.name = DataPointer(QuestionGroup, "name", I15dString)
QuestionGroup.color = DataAttribute(QuestionGroup, "color")
QuestionGroup.text_color = DataAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = DataPointerSet(QuestionGroup, "questions", Question)
