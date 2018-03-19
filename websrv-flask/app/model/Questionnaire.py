import os
from typing import List, Optional, Dict, Any

import yaml
from flask import g

from framework.exceptions import *
from framework.exceptions import YAMLTemplateInvalidException
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.I15dString import I15dString
from model.Question import Question
from model.QuestionGroup import QuestionGroup
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACModules import EMailVerificationQAC
from model.query_access_control.QACModules.TOSQAC import TOSQAC


class Questionnaire(DataObject):
    """
    A DataObject representing a Questionnaire.
    A Questionnaire is a collection of Questions which are grouped into
    QuestionGroups. A Questionnaire is targeted to a specific audience.
    It can have a number of Questionnaire Access Control Modules (QACModules)
    enabled on it.
    A Questionnaire is contained in a survey.
    """

    # needed to render questionnaires to anonymous users
    readable_by_anonymous = True

    ############################################################################
    # Factory and attribute related methods

    @staticmethod
    def create_questionnaire(name: str, description: str) -> "Questionnaire":
        """
        Factory method for Questionnaire, instantiates a new Questionnaire
        with default values.
        
        :param name: str The name of the new Questionnaire
        :param description: str The description text for the new Questionnaire
        :return: Questionnaire The new Questionnaire
        """
        questionnaire = Questionnaire()  # create new in db
        questionnaire.name = I15dString.new(name)
        questionnaire.description = I15dString.new(description)
        questionnaire.questiongroups = []
        questionnaire.question_count = 0
        questionnaire.answer_count = 0
        # These are the QACModules that are enabled by default when creating
        # a new Questionnaire
        questionnaire.qac_modules = [TOSQAC.new(), EMailVerificationQAC.new()]
        questionnaire.original_locale = g._locale
        questionnaire.published = False
        return questionnaire

    def set_name(self, name: str) -> None:
        """
        Setter for Questionnaire.name, wraps I15dString setter
        :param name: str The new name for the Questionnaire
        :return: None
        """
        self.name.set_locale(name)

    def set_description(self, description: str) -> None:
        """
        Setter for Questionnaire.description, wraps I15dString setter
        :param description: str The new description for the Questionnaire
        :return: None
        """
        self.description.set_locale(description)

    ############################################################################
    # Relationship related methods

    def add_question_group(self, name: str) -> QuestionGroup:
        """
        Adds a new QuestionGroup to the Questionnaire.
        :param name: str The name of the new QuestionGroup
        :return: QuestionGroup The newly created QuestionGroup
        """
        question_group = QuestionGroup.create_question_group(name)
        self.questiongroups.add(question_group)
        return question_group

    def remove_question_group(self, question_group: QuestionGroup) -> None:
        """
        Removes a QuestionGroup from the Questionnaire and deletes the
        QuestionGroup.
        :param question_group: QuestionGroup The QuestionGroup to remove 
        :return: None
        """
        self.questiongroups.remove(question_group)
        question_group.remove()

    def add_question_to_group(self, question_group: QuestionGroup,
                              text: str) -> Question:
        """
        Adds a new Question to a QuestionGroup of the Questionnaire.
        :param question_group: QuestionGroup The QuestioNGroup to add the 
                               Question to.
        :param text: str The Question text of the new Question
        :return: Question The newly created Question
        """
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
        """
        Removes a Question from a QuestionGroup of the Questionnaire.
        :param question_group: QuestionGroup The QuestionGroup the Question is 
                               in.
        :param question: Question The Question to remove
        :return: QuestionGroup The updated QuestionGroup
        """
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        question_group.remove_question(question)
        self.question_count -= 1
        return question_group

    ############################################################################
    # QAC related methods

    def get_qac_modules(self) -> List[QACModule]:
        """
        :return: List[QACModule] A list of QACModules that is enabled on this
                                 Questionnaire
        """
        return self.qac_modules

    def add_qac_module(self, qac_module: QACModule) -> None:
        """
        Adds a new qac module, if none with the same name exists.
        Raises QACAlreadyEnabledException if QAC already exists on this
        Questionnaire.
        :param qac_module: QACModule A QACModule instance to enable on this
                                     Questionnaire.
        """
        if qac_module.name.msgid not in [qac.name.msgid for qac in
                                         self.qac_modules]:
            self.qac_modules.add(qac_module)
        else:
            qac_module.remove()  # clean up unneeded qac_module from db

    def remove_qac_module(self, name: str) -> None:
        """
        Removes a qac module with the given name, if one exists.
        Actually removes all that fit, but it should always at most be one.
        Raises QACNotEnabledException when no matching QACModule was enabled
        on this Questionnaire.
        :param name: str The name (msgid) of the QACModule to remove.
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
        Returns the QACModule for the given name or None, if any exist.
        :param name: str The name of the QACModule to get 
        """
        for qac_module in self.qac_modules:
            if qac_module.name.msgid == name:
                return qac_module
        return None

    ############################################################################
    # YAML template related methods

    @staticmethod
    def parse_yaml(path_to_yaml: str) -> Dict[str, Any]:
        """
        Parses a YAMl template file for Questionnaire and raises Exceptions if
        the schema is invalid.
        :param path_to_yaml: str Path to the file to parse
        :return: dict The parsed YAML file.
        """
        with open(path_to_yaml) as fd:
            contents = yaml.load(fd)
        schema = {
            "name": str,
            "description": str,
            "questions": dict
        }
        try:
            if type(contents) != type(schema):
                raise Exception(_("Template needs to be a dictionary"))
            for k, v in schema.items():
                if k not in contents:
                    raise Exception(_("Missing argument in template: ") + k)
                if v != type(contents[k]):
                    raise Exception(_("Argument has wrong type: ") + k +
                                    _(" Expected: ") + str(v) +
                                    _(" Got: ") + str(type(contents[k])))
        except Exception as e:
            raise YAMLTemplateInvalidException(e.args[0])

        name = contents["name"]
        if len(name) < 1:
            raise YAMLTemplateInvalidException(_("Empty name specified"))

        return contents

    @staticmethod
    def get_available_templates() -> Dict[str, str]:
        """
        :return: dict A list of available template files a a dictionary of
                      {template_name: template_path}
        """
        template_files = dict({})
        for dirname, sdn, filenames in os.walk(
                g._config["SURVEY_TEMPLATE_PATH"]):
            for filename in filenames:
                abspath = os.path.join(dirname, filename)
                try:
                    contents = Questionnaire.parse_yaml(abspath)
                except Exception:
                    continue
                template_files[contents["name"]] = abspath
        return template_files

    @staticmethod
    def from_yaml(path_to_yaml: str) -> "Questionnaire":
        """
        Factory method for creating a Questionnaire from a YAML file.
        :param path_to_yaml: str Path to the YAML file to parse
        :return: Questionnaire The newly created Questionnaire
        """
        contents = Questionnaire.parse_yaml(path_to_yaml)
        new_questionnaire = Questionnaire.create_questionnaire(
            contents["name"],
            contents["description"]
        )
        for group_name, questions in contents["questions"].items():
            new_group = new_questionnaire.add_question_group(group_name)
            for question in questions:
                new_questionnaire.add_question_to_group(new_group, question)

        return new_questionnaire


Questionnaire.original_locale = DataAttribute(Questionnaire, "original_locale")
Questionnaire.name = DataPointer(Questionnaire, "name", I15dString)
Questionnaire.description = DataPointer(Questionnaire, "description",
                                             I15dString)
Questionnaire.questiongroups = DataPointerSet(
    Questionnaire, "questiongroups", QuestionGroup
)
Questionnaire.question_count = DataAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = DataAttribute(Questionnaire, "answer_count",
                                           no_acl=True)
Questionnaire.qac_modules = MixedDataPointerSet(Questionnaire, "qac_modules",
                                                serialize=False)
Questionnaire.published = DataAttribute(Questionnaire, "published")

# placed here to avoid cyclic imports
Question.questionnaire = DataPointer(Question, "questionnaire", Questionnaire)
