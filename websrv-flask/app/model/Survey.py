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

    def remove_questionnaire(self, name: str) -> None:
        length = len(self.questionnaires)
        # TODO: memory leak. the removed questionnaire is not removed from the db
        self.questionnaires = [x for x in self.questionnaires if not x.name == name]
        length_after = len(self.questionnaires)

        if length == length_after:
            raise QuestionnaireNotFoundException(self.name, name)


Survey.name = PersistentAttribute(Survey, "name")
Survey.date_created = PersistentAttribute(Survey, "date_created")
Survey.questionnaires = PersistentReferenceSet(Survey, "questionnaires", Questionnaire)
