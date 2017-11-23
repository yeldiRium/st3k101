from framework.exceptions import *
from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.Question import Question


class QuestionGroup(PersistentObject):
    def add_new_question(self, text: str) -> Question:
        question = Question()
        question.text = text
        self.questions.add(question)
        return question

    def remove_question(self, text: str):
        length = len(self.questions)
        # TODO: memory leak. the removed question is not deleted from the db
        self.questions = [x for x in self.questions if not x.text == text]
        length_after = len(self.questions)

        # if the length did not change, the question was not there
        if length == length_after:
            raise QuestionNotFoundException(self.name, text)

QuestionGroup.name = PersistentAttribute(QuestionGroup, "name")
QuestionGroup.color = PersistentAttribute(QuestionGroup, "color")
QuestionGroup.text_color = PersistentAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = PersistentReferenceSet(QuestionGroup, "questions", Question)
