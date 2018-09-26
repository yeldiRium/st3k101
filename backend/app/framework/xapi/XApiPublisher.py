import json
from typing import List

import requests

from framework.xapi.XApiStatement import XApiStatement
from utils.Singleton import Singleton

__author__ = "Noah Hummel"


class XApiPublisher(metaclass=Singleton):
    def __init__(self):
        self.__requests = []

    def flush(self):
        for url, payload in self.__requests:
            if payload:
                requests.post(url, json=json.dumps(payload))
            else:
                requests.post(url)

    def rollback(self):
        self.__requests = []

    def enqueue(self, statements: List[XApiStatement], receivers):
        payload = {
            'statements': [s.as_dict() for s in statements],
            'receivers': receivers
        }
        self.__requests.append((
            'http://xapi-publisher/enqueue/immediate',
            payload
        ))

    def enqueue_deferred(self, statements: List[XApiStatement], receivers, key):
        payload = {
            'statements': [s.as_dict() for s in statements],
            'receivers': receivers
        }

        self.__requests.append((
            'http://xapi-publisher/enqueue/deferred/{}'.format(key),
            payload
        ))

    def cancel(self, key):
        self.__requests.append(('http://xapi-publisher/cancel/{}'.format(key), None))

    def approve(self, key):
        self.__requests.append(('http://xapi-publisher/approve/{}'.format(key), None))
