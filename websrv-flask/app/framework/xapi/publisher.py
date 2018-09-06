import sys
from typing import Optional, List, Iterable

from requests_futures.sessions import FuturesSession
from flask import json, g

from framework.xapi.XApiStatement import XApiStatement

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

        publication = XApiPublication(statement, receivers)
        self.__publication_queue[publication.id] = publication

    def void(self, statement_id=None, *receivers: str):
        if statement_id is None:
            raise ValueError("No statement id provided.")

        statement = XApiVoidStatement(statement_id)
        self.enqueue(statement, *receivers)

    def publish(self):
        session = FuturesSession()
        headers = {
            'Content-Type': 'application/json',
            'X-Experience-API-Version': '1.0.0',
            'User-Agent': 'st3k101/2   .0'
        }

        def _settle_or_retry(publication_id, receiver, try_count):
            def _do_settle_or_retry(future):
                if future.exception() is None:  # settle
                    return

                publication = self.__publication_queue[publication_id]

                if try_count > g._config['XAPI_MAX_RETRIES']:
                    # save lost statement to disk
                    with open(g._config['XAPI_LOST_LOGFILE'], 'a') as f:
                        f.write("Lost statement for <{}> @ {}\n".format(receiver, publication.timestamp))
                        f.write("Statement was lost after {} unsuccessful transmissions.\n".format(try_count))
                        f.write(publication.json)
                        f.write("\n\n")

                _req = session.post(
                    receiver,
                    json=publication.json,
                    headers=headers
                )
                _req.add_done_callback(_settle_or_retry(publication_id, receiver, try_count + 1))

            return _do_settle_or_retry

        for publication in self.__publication_queue:
            for i_receiver in publication.receivers:
                req = session.post(
                    i_receiver, json=publication.json, headers=headers
                )
                req.add_done_callback(_settle_or_retry(publication.id, i_receiver, 0))

    def rollback(self):
        self.__publication_queue = dict()
