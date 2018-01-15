from typing import List

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.query_access_control.QACModule import QACModule


class Questionnaire(DataObject):
    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> QuestionGroup:
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
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

    def get_qac_module(self, name:str) -> QACModule:
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


Questionnaire.name = DataAttribute(Questionnaire, "name")
Questionnaire.description = DataAttribute(Questionnaire, "description")
Questionnaire.questiongroups = DataPointerSet(
    Questionnaire, "questiongroups", QuestionGroup
)
Questionnaire.question_count = DataAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = DataAttribute(Questionnaire, "answer_count")
Questionnaire.qac_modules = DataPointerSet(
    Questionnaire, "qac_modules", QACModule
)
