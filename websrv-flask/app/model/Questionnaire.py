from framework.exceptions import *
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model import Question
from model.QuestionGroup import QuestionGroup


class Questionnaire(DataObject):
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


Questionnaire.name = DataAttribute(Questionnaire, "name")
Questionnaire.description = DataAttribute(Questionnaire, "description")
Questionnaire.questiongroups = DataPointerSet(Questionnaire, "questiongroups", QuestionGroup)
Questionnaire.question_count = DataAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = DataAttribute(Questionnaire, "answer_count")
