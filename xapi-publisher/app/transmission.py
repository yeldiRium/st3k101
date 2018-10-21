import bson
import os
import random

from typing import Any, Dict, List, Tuple, Optional

from celery import Celery, chord
from datetime import datetime

from authentication.SharedReusableSession import SharedReusableSession, StaleSession
from authentication.methods import get_authentication_handler
from database import collection
from app import app

__author__ = "Noah Hummel"

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


class TransmissionBatch(object):
    def __init__(
            self,
            receiver: str,
            authentication_method: str,
            authentication_parameters: Dict[str, Any],
            statements: List[Tuple[str, str]]
    ):
        self.__receiver = receiver
        self.__authentication_method = authentication_method
        self.__authentication_parameters = authentication_parameters
        self.__statements = statements

    @property
    def receiver(self) -> str:
        return self.__receiver

    @property
    def authentication_method(self) -> str:
        return self.__authentication_method

    @property
    def authentication_parameters(self) -> Dict[str, Any]:
        return self.__authentication_parameters

    @property
    def statements(self) -> List[Tuple[str, str]]:
        return self.__statements


def create_batches(documents: List[Dict[str, Any]]) -> List[TransmissionBatch]:
    """
    Groups statements by receiver and authentication method, so that
    all statements with the same receiver and authentication method
    may be handled at once by the same session handler.
    :param documents: A list of documents from the database.
    :return: The grouped list in no particular order.
    """
    print("[TRANSMISSION] Creating batches ...")
    batches = dict()
    for document in documents:
        document_id = str(document['_id'])
        statement = document['statement']
        destination = document['destination']
        method = document['authentication']['method']
        parameters = document['authentication']['parameters']
        batch_id = hash((destination, method, frozenset(parameters.items())))
        if batch_id not in batches:
            print("[TRANSMISSION] New batch: {} for {} using {}".format(batch_id, destination, method))
            batches[batch_id] = {
                'destination': destination,
                'method': method,
                'parameters': parameters,
                'statements': []
            }
        batches[batch_id]['statements'].append((document_id, statement))
    return [TransmissionBatch(
        batch['destination'],
        batch['method'],
        batch['parameters'],
        batch['statements']
    ) for batch in batches.values()]


def find_and_lock() -> List[dict]:
    print("[TRANSMISSION] Locking documents for flush ...")
    flush_id = "{}--{}".format(datetime.now().isoformat(), os.urandom(32))
    collection.update_many(
        {'approved': True, 'in_flush': False},
        {'$set': {
            'in_flush': flush_id
        }}
    )  # lock statements that will be included in this flush
    return collection.find({'in_flush': flush_id})


@celery.task()
def flush():
    """
    Get all approved statements and schedule tasks for sending them.
    """
    print("[TRANSMISSION] Starting flush ...")
    documents = find_and_lock()
    for batch in create_batches(documents):
        authentication_handler = get_authentication_handler(batch.authentication_method)
        print("[TRANSMISSION] Starting batch for {} ({}) ...".format(batch.receiver, authentication_handler.__name__))
        session_handle = SharedReusableSession.get_handle(
            authentication_handler,
            batch.receiver,
            batch.authentication_parameters
        )
        try:
            session = SharedReusableSession(session_handle)
        except StaleSession:
            print("[TRANSMISSION] Stale session, renewing.")
            session = SharedReusableSession.new(
                authentication_handler,
                batch.receiver,
                batch.authentication_parameters
            )
        session_state = session.state
        batch_transmissions = [
            send_statement.si(
                batch.authentication_method,
                session_state,
                batch.receiver,
                document_id,
                statement)
            for document_id, statement in batch.statements
        ]
        chord(batch_transmissions)(handle_transmission_results.s(session_handle))


@celery.task()
def handle_transmission_results(results, session_handle):
    print("[TRANSMISSION] Collecting transmission results ...")
    should_retry = False
    auth_stale = False
    for document_id, status_code in results:
        document_id = bson.ObjectId(document_id)

        if status_code is None:
            print("[TRANSMISSION] Network failure detected on {}.".format(document_id))
            status_code = 666
        if status_code == 401:
            print("[TRANSMISSION] Authentication failure detected on {}.".format(document_id))
            auth_stale = True

        if 200 <= status_code < 300 or status_code == 409:
            print("[TRANSMISSION] Successfully transmitted {}.".format(document_id))
            collection.delete_one({'_id': document_id})
        else:
            print("[TRANSMISSION] Transmission failure detected on {} ({}).".format(document_id, status_code))
            document = collection.find_one({'_id': document_id})
            if document['transmission_attempts'] >= app.config['MAX_RETRIES']:
                print("[TRANSMISSION] Maximum number of retries exceeded for {}.".format(document_id))
                statement = document['statement']
                destination = document['destination']
                log_lost(statement, destination)
                collection.delete_one({'_id': document_id})
            else:
                collection.update_one(
                    {'_id': document_id},
                    {
                        '$set': {
                            'in_flush': False
                        },
                        '$inc': {
                            'transmission_attempts': 1
                        }
                    }
                )
                should_retry |= True

    if auth_stale:
        try:
            session = SharedReusableSession(session_handle)
            session.make_stale()
        except StaleSession:
            print("[TRANSMISSION] Auth was already stale.")

    if should_retry:
        min_delay = app.config['RETRY_MIN_INTERVAL']
        delay_time = random.uniform(0, 0.33 * min_delay) + min_delay
        flush.apply_async(countdown=delay_time)
        print("[TRANSMISSION] Retry scheduled in {}s".format(delay_time))


def log_lost(statement, receiver):
    print("[TRANSMISSION] Logging lost statement to file ...")
    with open(app.config['LOST_LOG'], 'a') as f:
        f.write("{}: lost xapi statement due to too many failed sending attempts.\n".format(datetime.now().isoformat()))
        f.write("Destination: {}\n".format(receiver))
        f.write(statement)
        f.write(2 * "\n")


@celery.task()
def send_statement(
        authentication_method: str,
        session_state: dict,
        destination: str,
        document_id: str,
        statement: str
) -> Tuple[str, Optional[int]]:
    authentication_handler = get_authentication_handler(authentication_method)
    status_code = authentication_handler.transmit_statement(
        destination,
        statement,
        session_state
    )
    return document_id, status_code
