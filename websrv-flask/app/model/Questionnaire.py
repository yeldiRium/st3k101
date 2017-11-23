from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.QuestionGroup import QuestionGroup


class Questionnaire(PersistentObject):
    def find_question_group_by_name(self, group_name: str) -> QuestionGroup:
        # TODO: refactor to use QuestionGroup.one_from_query()
        question_group = next((x for x in self.questiongroups if x.name == group_name), None)
        if question_group is None:
            raise QuestionGroupNotFoundException(self.name, group_name)
        return question_group

    def add_question_to_group(self, group_name: str, text: str) -> QuestionGroup:
        question_group = self.find_question_group_by_name(group_name)
        question_group.add_new_question(text)
        self.question_count += 1
        return question_group

    def remove_question_from_group(self, group_name: str, text: str) -> QuestionGroup:
        question_group = self.find_question_group_by_name(group_name)

        question_group.remove_question(text)

        self.question_count -= 1
        return question_group


Questionnaire.name = PersistentAttribute(Questionnaire, "name")
Questionnaire.description = PersistentAttribute(Questionnaire, "description")
Questionnaire.questiongroups = PersistentReferenceSet(Questionnaire, "questiongroups", QuestionGroup)
Questionnaire.question_count = PersistentAttribute(Questionnaire, "question_count")
