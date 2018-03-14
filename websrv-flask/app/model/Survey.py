from flask import g

from datetime import datetime

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from framework.internationalization import _
from model.DataClient import DataClient
from model.I15dString import I15dString
from model.Questionnaire import Questionnaire


class Survey(DataObject):
    """
    A DataObject representing a Survey.
    A Survey is a collection of Questionnaires, where each Questionnaire con-
    tains potentially different Questions and targets a specific audience in
    your survey.
    """

    @staticmethod
    def create_survey(name: str) -> "Survey":
        """
        Factory method for Survey, return a new instance of Survey initialized
        with default values.
        :param name: str The name of the survey
        :return: Survey the new instance
        """
        survey = Survey()
        survey.name = I15dString.new(name)
        survey.date_created = datetime.now().timestamp()
        survey.original_locale = g._locale
        return survey

    def set_name(self, name:str) -> None:
        """
        Setter method for Survey.name
        :param name: str The new name
        :return: None
        """
        self.name.set_locale(name)

    def add_new_questionnaire(self, name: str,
                              description: str) -> Questionnaire:
        """
        Creates and adds a new Questionnaire to this survey.
        :param name: str The name of the new Questionnaire
        :param description: str The description of the new Questionnaire
        :return: Questionnaire The newly created Questionnaire
        """
        questionnaire = Questionnaire.create_questionnaire(name, description)
        self.questionnaires.add(questionnaire)
        return questionnaire

    def add_new_questionnaire_from_template(
            self, name: str, description: str, template: str
    ) -> Questionnaire:
        """
        Creates a new Questionnaire by copying all settings from a given
        Questionnaire.
        
        :param name: str The name of the new Questionnaire
        :param description: str The description of the new Questionnaire
        :param template: str uuid of template file name of the template
        :return: Questionnaire The newly created Questionnaire
        """

        # first look in local template path
        template_files = Questionnaire.get_available_templates()

        if template in template_files:
            template_path = template_files[template]
            questionnaire = Questionnaire.from_yaml(template_path)
            self.questionnaires.add(questionnaire)
            return questionnaire

        # if template not found on disk try getting by uuid
        template_questionnaire = Questionnaire(template)

        # if template is in a different language, indicate that foreign
        # language was copied
        foreign_template = template_questionnaire.original_locale != g._locale
        template_locale = template_questionnaire.original_locale
        if foreign_template:
            name = _("From template: ") + name + " ({})".format(template_locale)
            description = _("From template: ") + description + " ({})".format(
                template_locale)

        questionnaire = self.add_new_questionnaire(name, description)

        for template_group in template_questionnaire.questiongroups:

            group_name = template_group.name.get_default_text()
            if foreign_template:
                group_name = _("From template: ") + group_name + "({})".format(
                    template_locale)

            new_group = questionnaire.add_question_group(group_name)
            new_group.color = template_group.color
            new_group.text_color = template_group.text_color

            for question in template_group.questions:
                question_text = question.text.get_default_text()
                if foreign_template:
                    question_text = _("From template: ") + question_text + \
                                    "({})".format(template_locale)

                questionnaire.add_question_to_group(new_group, question_text)

        for qac_module in template_questionnaire.qac_modules:
            questionnaire.add_qac_module(qac_module)
        return questionnaire

    def remove_questionnaire(self, questionnaire: Questionnaire) -> None:
        """
        Removes a questionnaire from this survey. Also removes the Questionnaire
        from the database
        :param questionnaire: Questionnaire The Qeustionnaire to remove from 
        the survey
        :return: None
        """
        try:
            self.questionnaires.remove(questionnaire)
            questionnaire.remove()
        except KeyError as _:
            raise QuestionnaireNotFoundException(
                self.name.get_default_text(), questionnaire.name.get_default_text())


Survey.original_locale = DataAttribute(Survey, "original_locale")
Survey.name = DataPointer(Survey, "name", I15dString)
Survey.date_created = DataAttribute(Survey, "date_created")
Survey.questionnaires = DataPointerSet(Survey, "questionnaires", Questionnaire)

# placed here to avoid cyclic import
DataClient.surveys = DataPointerSet(DataClient, "surveys", Survey,
                                    serialize=False)