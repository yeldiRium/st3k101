from typing import Dict, Any

from authentication.AuthenticationMethods import AuthenticationMethods
from database import collection

__author__ = "Noah Hummel"


def enqueue(statement, receivers, approval_key: int = None,
            authentication_method: AuthenticationMethods = AuthenticationMethods.NoAuthentication,
            authentication_parameters: Dict[str, Any] = None):
    if authentication_parameters is None:
        authentication_parameters = dict()
    document = {
        'approved': approval_key is None,
        'approval_key': approval_key,
        'receivers': receivers,
        'authentication_method': authentication_method.name,
        'authentication_parameters': authentication_parameters,
        'statement': statement
    }
    collection.insert_one(document)


def dequeue(survey_base_id: int=None):
    collection.delete_one({'approval_key': survey_base_id, 'approved': False})


def do_approve(survey_base_id: int=None):
    collection.update_many(
        {'approval_key': survey_base_id},
        {'$set': {
            'approved': True
        }}
    )