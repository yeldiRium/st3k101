from model.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceList
from model.Question import Question


class QuestionGroup(PersistentObject): pass

QuestionGroup.name = PersistentAttribute(QuestionGroup, "name")
QuestionGroup.color = PersistentAttribute(QuestionGroup, "color")
QuestionGroup.text_color = PersistentAttribute(QuestionGroup, "text_color")
QuestionGroup.questions = PersistentReferenceList(QuestionGroup, "questions", Question)
