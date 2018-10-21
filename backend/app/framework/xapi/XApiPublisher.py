import json

from flask import g
from typing import List

import requests

from framework.xapi.XApiStatement import XApiStatement
from utils.Singleton import Singleton

__author__ = "Noah Hummel"


class XApiPublisher(metaclass=Singleton):
    def __init__(self):
        self.__requests = []

    def __repr__(self):
        import pprint
        pp = pprint.PrettyPrinter()
        return object.__repr__(self) + "\n" + pp.pformat(self.__requests)

    def flush(self):
        for url, payload in self.__requests:
            if payload:
                requests.post(url, json=payload)
            else:
                requests.post(url)
        self.__requests = []  # avoid sending duplicates, yes that happened.

    def rollback(self):
        self.__requests = []

    def enqueue(self, statements: List[XApiStatement], receiver):
        payload = {
            'statements': [s.as_json() for s in statements],
            'receiver': receiver
        }
        if receiver == g._config['TLA_XAPI_ENDPOINT']:
            # TODO: hotfix for bachelor thesis, remove later
            payload['authentication'] = {
                'method': 'TLAFactsEngine',
                'parameters': {
                    'authentication_endpoint': g._config['TLA_AUTH_ENDPOINT'],
                    'username': g._config['TLA_AUTH_USERNAME'],
                    'password': g._config['TLA_AUTH_PASSWORD']
                }
            }
        self.__requests.append((
            'http://xapi-publisher/enqueue/immediate',
            payload
        ))

    def enqueue_deferred(self, statements: List[XApiStatement], receiver, key):
        payload = {
            'statements': [s.as_json() for s in statements],
            'receiver': receiver
        }
        if receiver == g._config['TLA_XAPI_ENDPOINT']:
            # TODO: hotfix for bachelor thesis, remove later
            payload['authentication'] = {
                'method': 'TLAFactsEngine',
                'parameters': {
                    'authentication_endpoint': g._config['TLA_AUTH_ENDPOINT'],
                    'username': g._config['TLA_AUTH_USERNAME'],
                    'password': g._config['TLA_AUTH_PASSWORD']
                }
            }

        self.__requests.append((
            'http://xapi-publisher/enqueue/deferred/{}'.format(key),
            payload
        ))

    def cancel(self, key):
        self.__requests.append(('http://xapi-publisher/cancel/{}'.format(key), None))

    def approve(self, key):
        self.__requests.append(('http://xapi-publisher/approve/{}'.format(key), None))
