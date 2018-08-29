import sys
from typing import Optional

from flask import json

from framework.xapi.XApiStatement import XApiStatement

__author__ = "Noah Hummel"


def publish_xapi_statement(statement: XApiStatement) -> str:
    print("=> XAPI: \n", json.dumps(statement.as_dict(), indent=4), file=sys.stderr)
    # TODO: use XApiPublisher


def query_xapi_statements(filter: dict) -> Optional[XApiStatement]:
    pass


def void_xapi_statement(statement_id: str=None, statement: XApiStatement=None):
    if statement_id is not None:
        pass
    elif statement is not None:
        pass
    else:
        raise ValueError("No statement or statement id provided.")
