from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
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
        self.questionnaires.add(questionnaire)
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
