from framework.signals import SIG_LOGGED_IN, SIG_ANSWER_SUBMITTED, SIG_ANSWER_VOIDED
from framework.xapi.publisher import XApiPublisher
from framework.xapi.statements.XApiAnswerSubmittedStatement import XApiAnswerSubmittedStatement
from framework.xapi.statements.XApiLoggedInStatement import XApiLoggedInStatement
from model.models.DataSubject import DataSubject
from model.models.Party import Party
from model.models.QuestionResponse import QuestionResponse
from utils import debug_print

__author__ = "Noah Hummel"


@SIG_LOGGED_IN.connect
def publish_logged_in_xapi_statement(sender: Party):
    statement = XApiLoggedInStatement(sender)
    XApiPublisher.get_instance().enqueue(statement)


@SIG_ANSWER_SUBMITTED.connect
def publish_answer_submitted_xapi_statement(
        sender: QuestionResponse
):
    question = sender.question
    subject = next(filter(lambda s: isinstance(s, DataSubject), sender.owners))
    receiver = question.dimension.questionnaire.xapi_target
    statement = XApiAnswerSubmittedStatement(subject, question, sender.value)
    sender.xapi_statement = statement.as_dict()
    XApiPublisher.get_instance().enqueue(statement, receiver)


@SIG_ANSWER_VOIDED.connect
def publish_answer_voided_xapi_statement(
        sender: QuestionResponse
):
    statement = sender.xapi_statement
    receiver = sender.question.dimension.questionnaire.xapi_target

    if statement is not None and 'id' in statement:
        debug_print("Found previous xAPI statement {}, voiding...".format(statement['id']))
        XApiPublisher.get_instance().void(statement['id'], receiver)
    else:
        debug_print("Something stinks.")
