import requests
from celery import Celery
from datetime import datetime
from requests import RequestException

from database import collection
from app import app

__author__ = "Noah Hummel"


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


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


def log_lost(statement, receiver):
    with open(app.config['LOST_LOG'], 'a') as f:
        f.write("{}: lost xapi statement due to too many failed sending attempts.\n".format(datetime.now().isoformat()))
        f.write("Destination: {}\n".format(receiver))
        f.write(statement)
        f.write(2*"\n")


class LogOnAbortTask(celery.Task):
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if status == "FAILURE":
            log_lost(*args)


@celery.task(
    base=LogOnAbortTask,
    autoretry_for=(AssertionError, RequestException),
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
    res = requests.post(receiver,
                        data=statement,
                        headers=headers,
                        timeout=5
                        )
    if res.status_code == 409:  # privacy settings don't match
        return  # DO NOT log the statement, privacy risk!
    assert 200 <= res.status_code < 300
    log_message = "{}: {}".format(receiver, res.status_code)
    if "Location" in res.headers:
        log_message += ", Location: {}".format(res.headers['Location'])
    print(log_message)
