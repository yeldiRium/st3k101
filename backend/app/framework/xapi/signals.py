from typing import Union

from framework.signals import SIG_LOGGED_IN, SIG_ANSWER_SUBMITTED
from framework.xapi.publisher import XApiPublisher
from framework.xapi.statements.XApiAnswerSubmittedStatement import XApiAnswerSubmittedStatement
from framework.xapi.statements.XApiLoggedInStatement import XApiLoggedInStatement
from model.models.DataSubject import DataSubject
from model.models.Party import Party
from model.models.QuestionResponse import QuestionResponse

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
    previous_results = filter(lambda r: r.verified, question.get_results_by_subject(subject))
    receiver = question.dimension.questionnaire.xapi_target

    for previous_result in previous_results:
        previous_statement = previous_result.xapi_statement
        if previous_statement is not None and 'id' in previous_statement:
            XApiPublisher.get_instance().void(previous_statement['id'], receiver)

    statement = XApiAnswerSubmittedStatement(subject, question, sender.value)
    XApiPublisher.get_instance().enqueue(statement, receiver)
