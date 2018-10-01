from datetime import datetime, timedelta

import requests
from celery import Celery

from flask import request, json, Response

from app import app
from database import collection


__author__ = "Noah Hummel"

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


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


def log_lost(statement, receiver):
    with open(app.config['LOST_LOG'], 'a') as f:
        f.write("{}: lost xapi statement due to too many failed sending attempts.\n".format(datetime.now().isoformat()))
        f.write("Destination: {}\n".format(receiver))
        f.write(json.dumps(statement))
        f.write(2*"\n")


def get_next_retry_time(retry_count):
    kappa = app.config['KAPPA']
    interval_seconds = (kappa * (retry_count + 1)) ** 2
    return datetime.now() + timedelta(seconds=interval_seconds)


class LogOnAbortTask(celery.Task):
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.max_retries == self.request.retries:
            log_lost(*args)


@celery.task(
    base=LogOnAbortTask,
    autoretry_for=(AssertionError,),
    retry_backoff=True,
    retry_kwargs={'max_retries': app.config['MAX_RETRIES']}
)
def send_statement(statement: dict, receiver: str):
    """
    Send a statement to a specific receiver, using at most MAX_RETRIES.
    Logs to LOST_LOG when MAX_RETRIES are exceeded.
    :param statement: An xAPI statement.
    :param receiver: An http(s) xAPI endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Experience-API-Version': '1.0.0',
        'User-Agent': 'st3k101/2.0'
    }
    payload = json.dumps(statement) if type(statement) is not str else statement
    req = requests.post(receiver, json=payload, headers=headers)
    assert req.status_code == 200


def flush():
    """
    Get all approved statements and schedule tasks for sending them.
    """
    documents = collection.find({'approved': True})
    for document in documents:
        receivers = document['receivers']
        statement = document['statement']

        for receiver in receivers:
            send_statement.delay(statement, receiver)
        collection.delete_one({'_id': document['_id']})


@app.route('/enqueue/immediate', methods=['POST'])
def enqueue_immediate():
    data = json.loads(request.json)
    statements = data['statements']
    receivers = data['receivers']
    for statement in statements:
        enqueue(statement, receivers)
    return "Success"


@app.route('/enqueue/deferred/<survey_base_id>', methods=['POST'])
def enqueue_deferred(survey_base_id: int=None):
    data = json.loads(request.json)
    statements = data['statements']
    receivers = data['receivers']
    for statement in statements:
        enqueue(statement, receivers, survey_base_id)
    return "Success"


@app.route('/approve/<survey_base_id>', methods=['POST'])
def approve(survey_base_id: int=None):
    do_approve(survey_base_id)
    return "Success"


@app.route('/cancel/<survey_base_id>', methods=['POST'])
def cancel(survey_base_id: int=None):
    dequeue(survey_base_id)
    return "Success"


@app.after_request
def after_request(response: Response):
    flush()
    return response
