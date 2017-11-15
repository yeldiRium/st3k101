from model.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceList
from model.QuestionGroup import QuestionGroup


class Questionnaire(PersistentObject): pass


Questionnaire.name = PersistentAttribute(Questionnaire, "name")
Questionnaire.questiongroups = PersistentReferenceList(Questionnaire, "questiongroups", QuestionGroup)
