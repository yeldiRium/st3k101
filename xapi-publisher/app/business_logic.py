from typing import Dict, Any

from database import collection

__author__ = "Noah Hummel"


def enqueue(statement, receiver, approval_key: int = None,
            authentication_method: str = "NoAuthentication",
            authentication_parameters: Dict[str, Any] = None):
    document = {
        'approved': approval_key is None,
        'approval_key': approval_key,
        'destination': receiver,
        'authentication': {
            'method': authentication_method,
            'parameters': authentication_parameters if authentication_parameters else dict()
        },
        'statement': statement,
        'transmission_attempts': 0,
        'in_flush': False
    }
    collection.insert_one(document)


def dequeue(survey_base_id: int = None):
    collection.delete_one({'approval_key': survey_base_id, 'approved': False})


def do_approve(survey_base_id: int = None):
    collection.update_many(
        {'approval_key': survey_base_id},
        {'$set': {
            'approved': True
        }}
    )
