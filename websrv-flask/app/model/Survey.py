from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire


class Survey(PersistentObject):
    def add_new_questionnaire(self, name: str, description: str) -> Questionnaire:
        questionnaire = next((x for x in self.questionnaires if x.name == name), None)
        if questionnaire is not None:
            raise DuplicateQuestionnaireNameException(self.name, name)

        questionnaire = Questionnaire()
        questionnaire.name = name
        questionnaire.description = description
        questionnaire.questiongroups = []
        questionnaire.question_count = 0
        questionnaire.answer_count = 0
        self.questionnaires.add(questionnaire)
        return questionnaire

    def add_new_questionnaire_from_template(
            self, name: str, description: str, template: Questionnaire
    ) -> Questionnaire:
        """
        Creates a new Questionnaire by copying all settings from a given
        Questionnaire.
        """
        questionnaire = self.add_new_questionnaire(name, description)
        for template_group in template.questiongroups:
            new_group = QuestionGroup()
            new_group.name = template_group.name
            new_group.color = template_group.color
            new_group.text_color = template_group.text_color
            questionnaire.questiongroups.add(new_group)
            for question in template_group.questions:
                questionnaire.add_question_to_group(new_group, question.text)
        return questionnaire

    def add_new_questionnaire_from_efla_student(
            self, name: str, description: str
    ) -> Questionnaire:
        """
        Alias for add_new_questionnaire_from_template with template for default
        efla_student questionnaire.
        """
        efla_student_template = None
        questionnaire = self.add_new_questionnaire_from_template(name, description, efla_student_template)
        return questionnaire

    def add_new_questionnaire_from_efla_teacher(
            self, name: str, description: str
    ) -> Questionnaire:
        """
        Alias for add_new_questionnaire_from_template with template for default
        efla_teacher questionnaire.
        """
        efla_teacher_template = None
        questionnaire = self.add_new_questionnaire_from_template(name, description, efla_teacher_template)
        return questionnaire

    def remove_questionnaire(self, questionnaire: Questionnaire) -> None:
        try:
            self.questionnaires.remove(questionnaire)
            questionnaire.remove()
        except KeyError as e:
            raise QuestionnaireNotFoundException(self.name, questionnaire.name)


Survey.name = PersistentAttribute(Survey, "name")
Survey.date_created = PersistentAttribute(Survey, "date_created")
Survey.questionnaires = PersistentReferenceSet(Survey, "questionnaires", Questionnaire)
