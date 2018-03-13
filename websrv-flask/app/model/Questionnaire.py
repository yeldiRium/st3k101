import os
from typing import List, Optional, Dict

import yaml
from flask import g

from framework.exceptions import *
from framework.exceptions import YAMLTemplateInvalidException
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _, babel_languages
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACModules import EMailVerificationQAC
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
        questionnaire.qac_modules = [TOSQAC.new(), EMailVerificationQAC.new()]
        questionnaire.original_locale = g._locale
        questionnaire.published = False
        return questionnaire

    def set_name(self, name):
        self.name.set_locale(name)

    def set_description(self, description):
        self.description.set_locale(description)

    def add_question_group(self, name):
        question_group = QuestionGroup.create_question_group(name)
        self.questiongroups.add(question_group)
        return question_group

    def remove_question_group(self, question_group: QuestionGroup):
        self.questiongroups.remove(question_group)
        question_group.remove()

    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> QuestionGroup:
        # text is always in surveys default locale
        # since adding new items to the survey is disabled in frontend
        # when user has switched to a different locale then the survey's
        # default locale
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        question = question_group.add_new_question(text)
        question.questionnaire = self
        self.question_count += 1
        return question

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
    def get_available_templates() -> Dict[str, List[str]]:
        template_files = {}
        for dirname, sdn, filenames in os.walk(
                g._config["SURVEY_TEMPLATE_PATH"]):
            for filename in filenames:
                template_files[filename] = os.path.join(dirname, filename)
        return template_files

    @staticmethod
    def from_yaml(path_to_yaml: str):
        schema = {
            "name": str,
            "language": str,
            "questions": dict
        }
        with open(path_to_yaml) as fd:
            contents = yaml.load(fd)
        try:
            if type(contents) != type(schema):
                raise Exception(_("Template needs to be a dictionary"))
            for k, v in schema.items():
                if k not in contents:
                    raise Exception(_("Missing argument in template: ") + k)
                if type(v) != type(contents[k]):
                    raise Exception(_("Argument has wrong type: ") + k +
                                    _(" Expected: ") + type(v) + _(" Got: ") +
                                    type(contents[k]))
        except Exception as e:
            raise YAMLTemplateInvalidException(e.args[0])

        language = contents["language"]
        if language not in babel_languages.keys():
            raise YAMLTemplateInvalidException(_("Invalid language specified"))

        name = contents["name"]
        if len(name) < 1:
            raise YAMLTemplateInvalidException(_("Empty name specified"))

        new_questionnaire = Questionnaire()
        for group_name, questions in contents["questions"].items():
            new_group = new_questionnaire.add_question_group(group_name)
            for question in questions:
                new_group.add_new_question(question)

        return new_questionnaire


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
Questionnaire.published = DataAttribute(Questionnaire, "published")

Question.questionnaire = DataPointer(Question, "questionnaire", Questionnaire)
