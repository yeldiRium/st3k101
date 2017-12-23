from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.Question import Question
from model.QuestionStatistic import QuestionStatistic


class QuestionGroup(PersistentObject):
    def add_new_question(self, text: str) -> Question:
        question = Question()
        question_statistic = QuestionStatistic()
        question_statistic.question = question
        question.text = text
        question.statistic = question_statistic
        self.questions.add(question)
        return question

    def remove_question(self, question: Question):
        try:
            self.questions.remove(question)
            question.remove()
        except KeyError as _:
            raise QuestionNotFoundException(self.name, question.text)

QuestionGroup.name = PersistentAttribute(QuestionGroup, "name")
QuestionGroup.color = PersistentAttribute(QuestionGroup, "color")
QuestionGroup.text_color = PersistentAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = PersistentReferenceSet(QuestionGroup, "questions", Question)
