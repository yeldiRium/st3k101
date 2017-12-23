from framework.odm.PersistentObject import PersistentObject, \
    PersistentAttribute, \
    PersistentReference
from model.QuestionStatistic import QuestionStatistic


class Question(PersistentObject): pass


# This is here to prevent circular dependencies in the QuestionStatistic.py file
QuestionStatistic.question = PersistentReference(QuestionStatistic, "question",
                                                 Question)

Question.text = PersistentAttribute(Question, "text")
Question.statistic = PersistentReference(Question, "statistic",
                                         QuestionStatistic)
