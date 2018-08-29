from framework.signals import SIG_LOGGED_IN
from framework.xapi.publisher import publish_xapi_statement
from framework.xapi.statements.XApiLoggedInStatement import XApiLoggedInStatement
from model.models.DataClient import DataClient

__author__ = "Noah Hummel"


@SIG_LOGGED_IN.connect
def publish_logged_in_xapi_statement(sender: DataClient):
    statement = XApiLoggedInStatement(sender)
    publish_xapi_statement(statement)
