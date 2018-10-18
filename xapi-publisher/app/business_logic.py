from datetime import datetime

from database import collection

__author__ = "Noah Hummel"


def enqueue(statement, receivers, survey_base_id: int=None):
    document = {
        'approved': survey_base_id is None,
        'approval_key': survey_base_id,
        'receivers': receivers,
        'statement': statement,
        'retry_count': 0,
        'retry_after': datetime.now()
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