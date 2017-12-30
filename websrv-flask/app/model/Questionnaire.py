from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.Question import Question
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

    @staticmethod
    def get_efla_student_template():
        template = Questionnaire.one_from_query({"name": "efla_student_template"})
        if template is None:
            pass  # TODO: create template
        else:
            return template

    @staticmethod
    def get_efla_teacher_template():
        template = Questionnaire.one_from_query({"name": "efla_teacher_template"})
        if template is None:
            pass  # TODO: create template
        else:
            return template


Questionnaire.name = PersistentAttribute(Questionnaire, "name")
Questionnaire.description = PersistentAttribute(Questionnaire, "description")
Questionnaire.questiongroups = PersistentReferenceSet(Questionnaire, "questiongroups", QuestionGroup)
Questionnaire.question_count = PersistentAttribute(Questionnaire, "question_count")
Questionnaire.answer_count = PersistentAttribute(Questionnaire, "answer_count")
