from api.utils.ResourceBroker import ResourceBroker
from framework.xapi.XApiActivities import XApiActivities
from framework.xapi.XApiActor import XApiMboxActor, XApiAccountActor
from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiActivityObject
from framework.xapi.XApiResult import XApiScoredResult
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from framework.xapi.statements.utils import get_party_as_actor, get_xapi_object
from model.models.DataSubject import DataSubject
from model.models.Question import Question

__author__ = "Noah Hummel"


class XApiAnswerSubmittedStatement(XApiStatement):

    def __init__(self, datasubject: DataSubject, question: Question, value: int):
        super(XApiAnswerSubmittedStatement, self).__init__(
            get_party_as_actor(datasubject),
            XApiVerb(XApiVerbs.Answered),
            get_xapi_object(question),
            xapi_context=XApiSt3k101Context(),
            xapi_result=XApiScoredResult(value, question.range_start, question.range_end, 1)
        )
