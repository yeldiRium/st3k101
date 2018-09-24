from framework.dependency_injection import ResourceBroker
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiActor import XApiMboxActor
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from model.models.DataSubject import DataSubject
from model.models.Question import Question

__author__ = "Noah Hummel"


class XApiAnswerSubmittedStatement(XApiStatement):

    def __init__(self, datasubject: DataSubject, question: Question, value: int):
        super(XApiAnswerSubmittedStatement, self).__init__(
            XApiMboxActor(datasubject.email, datasubject.email),
            XApiVerb(XApiVerbs.SubmittedAnswer),
            XApiActivityObject(
                XApiActivities.Question,
                ResourceBroker.url_for(question),
                question.name_translations
            )
        )
