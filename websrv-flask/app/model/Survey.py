from flask import g

from datetime import datetime

from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString
from model.Questionnaire import Questionnaire


class Survey(DataObject):
    exposed_properties = {
        "name"
    }

    @staticmethod
    def create_survey(name: str):
        survey = Survey()
        survey.i15d_name = I15dString()
        survey.name = name
        survey.date_created = datetime.now().timestamp()
        survey.original_locale = g._locale.name
        return survey

    def add_new_questionnaire(self, name: str,
                              description: str) -> Questionnaire:
        if next((x for x in self.questionnaires if x.name == name),
                None) is not None:
            raise DuplicateQuestionnaireNameException(self.name, name)

        questionnaire = Questionnaire.create_questionnaire(name, description)
        self.questionnaires.add(questionnaire)
        return questionnaire

    def add_new_questionnaire_from_template(
            self, name: str, description: str, template: str
    ) -> Questionnaire:
        """
        Creates a new Questionnaire by copying all settings from a given
        Questionnaire.
        """
        if template == "efla_teacher":
            template_questionnaire = Questionnaire.get_efla_teacher_template()
        elif template == "efla_student":
            template_questionnaire = Questionnaire.get_efla_student_template()
        else:
            template_questionnaire = Questionnaire(template)

        questionnaire = self.add_new_questionnaire(name, description)
        for template_group in template_questionnaire.questiongroups:
            new_group = questionnaire.add_question_group(template_group.name)
            new_group.color = template_group.color
            new_group.text_color = template_group.text_color
            for question in template_group.questions:
                questionnaire.add_question_to_group(new_group, question.text)
        for qac_module in template_questionnaire.qac_modules:
            questionnaire.add_qac_module(qac_module)
        return questionnaire

    def remove_questionnaire(self, questionnaire: Questionnaire) -> None:
        try:
            self.questionnaires.remove(questionnaire)
            questionnaire.remove()
        except KeyError as e:
            raise QuestionnaireNotFoundException(self.name, questionnaire.name)

    @property
    def name(self):
        return self.i15d_name.get()

    @name.setter
    def name(self, name: str):
        self.i15d_name.add_locale(g._locale, name)


Survey.original_locale = DataAttribute(Survey, "original_locale")
Survey.i15d_name = DataPointer(Survey, "i15d_name", I15dString, serialize=False)
Survey.date_created = DataAttribute(Survey, "date_created")
Survey.questionnaires = DataPointerSet(Survey, "questionnaires", Questionnaire)
