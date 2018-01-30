from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataAttribute import DataAttribute
from model.DataSubject import DataSubject


class QuestionResult(DataObject): pass


QuestionResult.subject_confirmed = DataAttribute(QuestionResult, "subject_confirmed", serialize=False)
QuestionResult.data_subject = DataPointer(QuestionResult, "data_subject", DataSubject)
QuestionResult.answer_value = DataAttribute(QuestionResult, "answer_value")
