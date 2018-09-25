from uuid import UUID

from framework.xapi.XApiContext import XApiSt3k101Context
from framework.xapi.XApiObject import XApiStatementRefObject
from framework.xapi.XApiStatement import XApiStatement
from framework.xapi.XApiVerb import XApiVerb
from framework.xapi.XApiVerbs import XApiVerbs
from framework.xapi.statements.utils import get_current_user_as_actor

__author__ = "Noah Hummel"


class XApiVoidStatement(XApiStatement):
    def __init__(self, statement_id: UUID):
        super(XApiVoidStatement, self).__init__(
            get_current_user_as_actor(),
            XApiVerb(XApiVerbs.Voided),
            XApiStatementRefObject(statement_id=statement_id),
            xapi_context=XApiSt3k101Context()
        )
