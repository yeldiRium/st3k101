from model.DataSubject import DataSubject
from model.PersistentObject import PersistentObject, PersistentReference, PersistentAttribute
from model.Question import Question


class QuestionResult(PersistentObject): pass


QuestionResult.question = PersistentReference(QuestionResult, "question", Question)
QuestionResult.data_subject = PersistentReference(QuestionResult, "question", DataSubject)
QuestionResult.answer_value = PersistentAttribute(QuestionResult, "answer_value")
