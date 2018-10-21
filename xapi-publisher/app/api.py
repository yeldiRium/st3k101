from flask import request

from authentication import methods
from app import app
from business_logic import enqueue, do_approve, dequeue

__author__ = "Noah Hummel"


@app.route('/authentication/methods', methods=['GET'])
def get_available_authentication_methods():
    return methods.get_available_authentication_methods()


@app.route('/enqueue/immediate', methods=['POST'])
def enqueue_immediate():
    statements = request.json['statements']
    receivers = request.json['receivers']
    authentication_args = []
    if 'authentication' in request.json:
        authentication = request.json['authentication']
        authentication_args = [
            authentication['method'],
            authentication['parameters']
        ]
    for statement in statements:
        enqueue(statement, receivers, None, *authentication_args)
    return "Success"


@app.route('/enqueue/deferred/<survey_base_id>', methods=['POST'])
def enqueue_deferred(survey_base_id: int=None):
    statements = request.json['statements']
    receivers = request.json['receivers']
    authentication_args = []
    if 'authentication' in request.json:
        authentication = request.json['authentication']
        authentication_args = [
            authentication['method'],
            authentication['parameters']
        ]
    for statement in statements:
        enqueue(statement, receivers, survey_base_id, *authentication_args)
    return "Success"


@app.route('/approve/<survey_base_id>', methods=['POST'])
def approve(survey_base_id: int=None):
    do_approve(survey_base_id)
    return "Success"


@app.route('/cancel/<survey_base_id>', methods=['POST'])
def cancel(survey_base_id: int=None):
    dequeue(survey_base_id)
    return "Success"

