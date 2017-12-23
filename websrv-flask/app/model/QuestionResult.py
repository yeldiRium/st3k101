from framework.odm.PersistentObject import PersistentObject, PersistentReference, PersistentAttribute
from model.DataSubject import DataSubject


class QuestionResult(PersistentObject): pass


QuestionResult.data_subject = PersistentReference(QuestionResult, "data_subject", DataSubject)
QuestionResult.answer_value = PersistentAttribute(QuestionResult, "answer_value")
