from typing import List, Optional

from flask import g

from framework.exceptions import *
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACModules.TOSQAC import TOSQAC


class Questionnaire(DataObject):

    readable_by_anonymous = True

    @staticmethod
    def create_questionnaire(name: str, description: str):
        questionnaire = Questionnaire()
        questionnaire.name = I15dString()
        questionnaire.name.set_locale(name)
        questionnaire.description = I15dString()
        questionnaire.description.set_locale(description)
        questionnaire.questiongroups = []
        questionnaire.question_count = 0
        questionnaire.answer_count = 0
        questionnaire.qac_modules = [TOSQAC.new()]
        questionnaire.original_locale = g._locale
        return questionnaire

    def add_question_group(self, name):
        if next((x for x in self.questiongroups if x.name.get_default_text() == name),
                None) is not None:
            raise DuplicateQuestionGroupNameException()

        question_group = QuestionGroup.create_question_group(name)
        self.questiongroups.add(question_group)
        return question_group

    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> QuestionGroup:
        # text is always in surveys default locale
        # since adding new items to the survey is disabled in frontend
        # when user has switched to a different locale then the survey's
        # default locale
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        for question in question_group.questions:
            if question.text.get_default_text() == text:
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
        Raises QACAlreadyEnabledException if QAC already exists on this
        Questionnaire.
        """
        if qac_module.name.msgid not in [qac.name.msgid for qac in self.qac_modules]:
            self.qac_modules.add(qac_module)
        else:
            qac_module.remove()  # clean up unneeded quac_module from db
            raise QACAlreadyEnabledException()

    def remove_qac_module(self, name: str):
        """
        Removes a qac module with the given name, if one exists.
        Actually removes all that fit, but it should always at most be one.
        Raises QACNotEnabledException when no matching QACModule was enabled
        on this Questionnaire.
        """
        deleted_count = 0
        for qac_module in self.qac_modules:
            if qac_module.name.msgid == name:
                self.qac_modules.remove(qac_module)
                qac_module.remove()  # delete qac_module from database
                deleted_count += 1

        if deleted_count < 1:
            raise QACNotEnabledException()

    def get_qac_module(self, name: str) -> Optional[QACModule]:
        """
        Returns the QACModule for the given name or None, if none exists.
        """
        for qac_module in self.qac_modules:
            if qac_module.name.msgid == name:
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


Questionnaire.original_locale = DataAttribute(Questionnaire, "original_locale")
Questionnaire.name = DataPointer(Questionnaire, "name", I15dString)
Questionnaire.description = DataPointer(Questionnaire, "description",
                                             I15dString)
Questionnaire.questiongroups = DataPointerSet(
    Questionnaire, "questiongroups", QuestionGroup
)
Questionnaire.question_count = DataAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = DataAttribute(Questionnaire, "answer_count")
Questionnaire.qac_modules = MixedDataPointerSet(Questionnaire, "qac_modules",
                                                serialize=False)
