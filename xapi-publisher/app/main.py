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
        'receivers': [
            {
                'receiver': receiver,
                'retry_count': 0,
                'retry_after': datetime.now()
            } for receiver in receivers
        ],
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


@celery.task
def flush():
    documents = collection.find({'approved': True})
    headers = {
        'Content-Type': 'application/json',
        'X-Experience-API-Version': '1.0.0',
        'User-Agent': 'st3k101/2.0'
    }

    sent = []
    for document in documents:
        receivers = document['receivers']
        statement = document['statement']

        unavailable_receivers = []
        for receiver_info in receivers:
            receiver = receiver_info['receiver']
            retry_count = receiver_info['retry_count']
            retry_after = receiver_info['retry_after']

            if retry_count > app.config['MAX_RETRIES']:
                # drop statement after MAX_RETRIES
                log_lost(statement, receiver)
                sent.append(document)
                continue

            if datetime.now() <= retry_after:
                continue

            req = requests.post(
                receiver, json=statement, headers=headers
            )
            if req.status_code != 200:
                unavailable_receivers.append({
                    'receiver': receiver,
                    'retry_count': retry_count + 1,
                    'retry_after': get_next_retry_time(retry_count)
                })

        if not unavailable_receivers:  # all sent successfully
            sent.append(document)
        else:
            collection.update_one(
                {'_id': document['_id']},
                {'$set': {
                    'receivers': unavailable_receivers
                }}
            )
    for document in sent:
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
    flush.delay()  # TODO: if no new statements are sent, no retries are performed, use celery beat
    return response
