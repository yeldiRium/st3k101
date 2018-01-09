from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.QuestionGroup import QuestionGroup
from model.Questionnaire import Questionnaire


class Survey(DataObject):
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
            new_group = QuestionGroup()
            new_group.name = template_group.name
            new_group.color = template_group.color
            new_group.text_color = template_group.text_color
            questionnaire.questiongroups.add(new_group)
            for question in template_group.questions:
                questionnaire.add_question_to_group(new_group, question.text)
        return questionnaire

    def remove_questionnaire(self, questionnaire: Questionnaire) -> None:
        try:
            self.questionnaires.remove(questionnaire)
            questionnaire.remove()
        except KeyError as e:
            raise QuestionnaireNotFoundException(self.name, questionnaire.name)


Survey.name = DataAttribute(Survey, "name")
Survey.date_created = DataAttribute(Survey, "date_created")
Survey.questionnaires = DataPointerSet(Survey, "questionnaires", Questionnaire)
