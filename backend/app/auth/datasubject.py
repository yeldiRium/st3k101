from flask import g
from time import time
import os
from typing import Optional

from auth.users import PartyTypes
from auth import session
from framework.memcached import get_memcache
from model.models.DataSubject import DataSubject

__author__ = "Noah Hummel"


def _get_auth_request_mc_key(email: str) -> str:
    return 'auth.sessions.datasubject.auth_start.{}'.format(email)


def get_auth_request(email: str) -> Optional[dict]:
    mc = get_memcache()
    return mc.get(_get_auth_request_mc_key(email))


def new_auth_request(email: str) -> dict:
    """
    Starts the email validation mechanism for logging in DataSubjects.
    This will send an email to the DataSubject, provided a DataSubject
    with that email exists. Does not send an email, if another email
    has been sent in the previous 5 minutes. The request is valid for 20 minutes
    before being invalidated.
    :param email: str The DataSubject's email address
    :return: dict The request body
    """
    key = _get_auth_request_mc_key(email)
    request = {
        'email': email,
        'token': os.urandom(32).hex(),
        'timestamp': time()
    }
    mc = get_memcache()
    return mc.set(key, request, time=g._config['AUTH_REQUEST_TTL']) != 0


def cancel_auth_request(email: str) -> bool:
    mc = get_memcache()
    return mc.delete(_get_auth_request_mc_key(email)) != 0


def complete_auth_request(email: str, token: str) -> Optional[str]:
    request = get_auth_request(email)
    if request is None:
        return None

    if request['token'] != token:
        return None

    subject = DataSubject.query.filter_by(email=email).first()
    if subject is None:
        return None

    cancel_auth_request(email)

    return session.new(subject.id, PartyTypes.DataSubject)


def new_lti_session(lti_user_id: str) -> Optional[str]:
    subject = DataSubject.query.filter_by(lti_user_id=lti_user_id).first()
    if subject is None:
        return None

    return session.new(subject.id, PartyTypes.DataSubject)
