import requests
from flask import Flask, request, json

from database import collection


__author__ = "Noah Hummel"


app = Flask(__name__)


def enqueue(statement, receivers, survey_base_id: int=None):
    document = {
        'approved': survey_base_id is None,
        'approval_key': survey_base_id,
        'receivers': receivers,
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
        for receiver in receivers:
            req = requests.post(
                receiver, json=statement, headers=headers
            )
            if req.status_code != 200:
                unavailable_receivers.append(receiver)

        if not unavailable_receivers:
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
def after_request():
    flush()
