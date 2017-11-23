from framework.odm.PersistentObject import PersistentObject, PersistentAttribute


class Question(PersistentObject): pass


Question.text = PersistentAttribute(Question, "text")
