from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceList
from model.Question import Question


class QuestionGroup(PersistentObject):
    def add_new_question(self, text: str):
        question = Question()
        question.text = text
        self.questions.add(question)

    def remove_question(self, text: str):
        length = len(self.questions)
        self.questions = [x for x in self.questions if not x.text == text]
        length_after = len(self.questions)

        # if the length did not change, the question was not there
        if length == length_after:
            raise QuestionNotFoundException(self.name, text)

QuestionGroup.name = PersistentAttribute(QuestionGroup, "name")
QuestionGroup.color = PersistentAttribute(QuestionGroup, "color")
QuestionGroup.text_color = PersistentAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = PersistentReferenceList(QuestionGroup, "questions", Question)
