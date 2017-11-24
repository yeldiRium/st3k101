from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model import Question
from model.QuestionGroup import QuestionGroup


class Questionnaire(PersistentObject):
    def add_question_to_group(self, question_group: QuestionGroup, text: str) -> QuestionGroup:
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        question_group.add_new_question(text)
        self.question_count += 1
        return question_group

    def remove_question_from_group(self, question_group: QuestionGroup, question: Question) -> QuestionGroup:
        if question_group not in self.questiongroups:
            raise QuestionGroupNotFoundException
        question_group.remove_question(question)
        self.question_count -= 1
        return question_group


Questionnaire.name = PersistentAttribute(Questionnaire, "name")
Questionnaire.description = PersistentAttribute(Questionnaire, "description")
Questionnaire.questiongroups = PersistentReferenceSet(Questionnaire, "questiongroups", QuestionGroup)
Questionnaire.question_count = PersistentAttribute(Questionnaire, "question_count")
