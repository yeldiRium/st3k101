from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class Question(DataObject): pass


Question.text = DataAttribute(Question, "text")
