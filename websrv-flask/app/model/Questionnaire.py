from typing import List

from flask import g

from framework.exceptions import *
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.query_access_control.QACModule import QACModule


class Questionnaire(DataObject):
    exposed_properties = {
        "name",
        "description"
    }

    @staticmethod
    def create_questionnaire(name: str, description: str):
        questionnaire = Questionnaire()
        questionnaire.i15d_name = I15dString()
        questionnaire.name = name
        questionnaire.i15d_description = I15dString()
        questionnaire.description = description
        questionnaire.questiongroups = []
        questionnaire.question_count = 0
        questionnaire.answer_count = 0
        questionnaire.qac_modules = []
        return questionnaire

    def add_question_group(self, name):
        if next((x for x in self.questiongroups if x.name == name),
                None) is not None:
            raise DuplicateQuestionGroupNameException()

        question_group = QuestionGroup.create_question_group(name)
        self.questiongroups.add(question_group)
        return question_group

    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> QuestionGroup:
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        for question in question_group.questions:
            if question.text == text:
                raise DuplicateQuestionNameException()
        question_group.add_new_question(text)
        self.question_count += 1
        return question_group

    def remove_question_from_group(self, question_group: QuestionGroup,
                                   question: Question) -> QuestionGroup:
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        question_group.remove_question(question)
        self.question_count -= 1
        return question_group

    def get_qac_modules(self) -> List[QACModule]:
        return self.qac_modules

    def add_qac_module(self, qac_module: QACModule):
        """
        Adds a new qac module, if none with the same name exists.
        """
        if qac_module.get_name() not in [x.get_name() for x in
                                         self.qac_modules]:
            self.qac_modules.add(qac_module)

    def remove_qac_module(self, name: str):
        """
        Removes a qac module with the given name, if one exists.
        Actually removes all that fit, but it should always at most be one.
        """
        for qac_module in self.qac_modules:
            if qac_module.get_name() == name:
                self.qac_modules.remove(qac_module)

    def get_qac_module(self, name: str) -> QACModule:
        """
        Returns the QACModule for the given name or None, if none exists.
        """
        for qac_module in self.qac_modules:
            if qac_module.get_name() == name:
                return qac_module
        return None

    @staticmethod
    def get_efla_student_template():
        template = Questionnaire.one_from_query(
            {"name": "efla_student_template"})
        if template is None:
            pass  # TODO: create template
        else:
            return template

    @staticmethod
    def get_efla_teacher_template():
        template = Questionnaire.one_from_query(
            {"name": "efla_teacher_template"})
        if template is None:
            pass  # TODO: create template
        else:
            return template

    @property
    def name(self):
        return self.i15d_name.get()

    @name.setter
    def name(self, name: str):
        self.i15d_name.add_locale(g._current_user._locale, name)

    @property
    def description(self):
        return self.i15d_description.get()

    @description.setter
    def description(self, description: str):
        self.i15d_description.add_locale(g._current_user._locale, description)


Questionnaire.i15d_name = DataPointer(Questionnaire, "i15d_name", I15dString,
                                      serialize=False)
Questionnaire.i15d_description = DataPointer(Questionnaire, "description",
                                             I15dString, serialize=False)
Questionnaire.questiongroups = DataPointerSet(
    Questionnaire, "questiongroups", QuestionGroup
)
Questionnaire.question_count = DataAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = DataAttribute(Questionnaire, "answer_count")
Questionnaire.qac_modules = DataPointerSet(
    Questionnaire, "qac_modules", QACModule
)
