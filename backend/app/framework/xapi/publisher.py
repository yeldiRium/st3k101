from datetime import datetime

import requests
from typing import Optional, List, Iterable

from flask import json, g

from framework.xapi.XApiStatement import XApiStatement
from utils import debug_print

__author__ = "Noah Hummel"


class XApiPublication(object):
    def __init__(self, statement: XApiStatement, receivers: Iterable[str]):
        self.__statement = statement
        self.__receivers = receivers

    @property
    def statement(self) -> XApiStatement:
        return self.__statement

    @property
    def json(self):
        return self.__statement.as_json()

    @property
    def id(self):
        return self.__statement.as_dict()['id']

    @property
    def timestamp(self):
        return self.__statement.as_dict()['timestamp']

    @property
    def receivers(self) -> Iterable[str]:
        return self.__receivers


class XApiPublisher(object):
    __instance = None

    @staticmethod
    def get_instance():
        if XApiPublisher.__instance is None:
            XApiPublisher.__instance = XApiPublisher()
        return XApiPublisher.__instance

    def __init__(self):
        if self.__instance is not None:
            raise RuntimeError
        self.__publication_queue = {}

    def enqueue(self, statement, *receivers: str):
        if not receivers:
            receivers = [g._config['XAPI_DEFAULT_TARGET']]

        debug_print("XApiPublisher: Enqueueing statement {} for {}.".format(statement.get_id(), receivers))

        publication = XApiPublication(statement, receivers)
        self.__publication_queue[publication.id] = publication

    def void(self, statement_id=None, *receivers: str):
        if statement_id is None:
            raise ValueError("No statement id provided.")

        statement = XApiVoidStatement(statement_id)
        self.enqueue(statement, *receivers)

    def publish(self):
        debug_print("Publishing xapi statements...")
        headers = {
            'Content-Type': 'application/json',
            'X-Experience-API-Version': '1.0.0',
            'User-Agent': 'st3k101/2.0'
        }
        debug_print(self.__publication_queue)
        to_send = set()
        sent = set()
        for publication_id, publication in self.__publication_queue.items():
            for receiver in publication.receivers:
                to_send.add((publication_id, receiver))
        debug_print(to_send)

        max_retries = g._config['XAPI_MAX_RETRIES']
        for _ in range(max_retries):
            for item in sent:
                to_send.discard(item)

            if len(to_send) == 0:
                break

            for publication_id, receiver in to_send:
                publication = self.__publication_queue[publication_id]
                req = requests.post(
                    receiver, json=publication.json, headers=headers
                )
                if req.status_code == 200:
                    sent.add((publication_id, receiver))

        for lost_id, unavailable_receiver in to_send:
            lost_publication = self.__publication_queue[lost_id]
            debug_print("XApiPublisher: LOST xAPI statement {} for {}".format(lost_id, unavailable_receiver))
            with open(g._config['XAPI_LOST_LOG'], 'a') as lost_log:
                lost_log.write(datetime.now().isoformat())
                lost_log.write(": lost xAPI statement after {} attempts to send.\n".format(max_retries))
                lost_log.write("Destination: {}\n".format(unavailable_receiver))
                lost_log.write("Statement:\n")
                lost_log.write(lost_publication.json)
                lost_log.write("\nEnd of statement.\n\n")

    def rollback(self):
        self.__publication_queue = dict()
