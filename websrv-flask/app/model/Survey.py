from model.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceList
from model.Questionnaire import Questionnaire


class Survey(PersistentObject): pass


Survey.name = PersistentAttribute(Survey, "name")
Survey.date_created = PersistentAttribute(Survey, "date_created")
Survey.questionnaires = PersistentReferenceList(Survey, "questionnaires", Questionnaire)
