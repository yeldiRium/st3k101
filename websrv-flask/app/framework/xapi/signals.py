from framework.signals import SIG_LOGGED_IN, SIG_ANSWER_SUBMITTED
from framework.xapi.publisher import publish_xapi_statement, void_xapi_statement
from framework.xapi.statements.XApiAnswerSubmittedStatement import XApiAnswerSubmittedStatement
from framework.xapi.statements.XApiLoggedInStatement import XApiLoggedInStatement
from model.models.DataClient import DataClient
from model.models.DataSubject import DataSubject
from model.models.Question import Question

__author__ = "Noah Hummel"


@SIG_LOGGED_IN.connect
def publish_logged_in_xapi_statement(sender: DataClient):
    statement = XApiLoggedInStatement(sender)
    publish_xapi_statement(statement)


@SIG_ANSWER_SUBMITTED.connect
def publish_answer_submitted_statement(
        sender: DataSubject,
        question: Question,
        value: int
):
    previous_results = filter(lambda r: r.verified, question.get_results_by_subject(sender))
    for previous_result in previous_results:
        previous_statement = previous_result.xapi_statement
        if previous_statement is not None and 'id' in previous_statement:
            void_xapi_statement(statement_id=previous_statement['id'])

    statement = XApiAnswerSubmittedStatement(sender, question, value)
    publish_xapi_statement(statement)