import os
from flask import g

from typing import Optional

import time

from auth import MEMCACHED_PREFIX
from auth.users import PartyTypes
from framework import get_client_ip
from framework.exceptions import ClientIpChangedException, UserNotLoggedInException
from framework.memcached import get_memcache
from utils import debug_print

__author__ = "Noah Hummel"


def _build_session_record(party_id: int, party_type: PartyTypes, ttl: int=1800):
    assert party_type in PartyTypes
    return _serialize_session_record({
        'uuid': party_id,
        'type': party_type,
        'ttl': ttl,
        'last_seen': time.time(),
        'client_ip': get_client_ip()
    })


def _serialize_session_record(record: dict) -> Optional[dict]:
    if record is None:
        return None
    record['type'] = record['type'].name
    return record


def _deserialize_session_record(record: dict) -> Optional[dict]:
    if record is None:
        return None
    record['type'] = PartyTypes[record['type']]
    return record


def _get_session_record_id(session_token: str) -> str:
    """
    Returns the name of the key used in memcached to identify the session record
    with the given session_token
    :param session_token: str A session token
    :return: str
    """
    return MEMCACHED_PREFIX + "sessions." + session_token


def get_session_record(session_token: str) -> dict:
    """
    Returns the session record for the given session token.
    The record has the form:
    record := {
        'last_seen': int,  # timestamp
        'ttl': int,  # maximum time with no activity
        'uuid':  str,  # hex representation of DataClient ObjectId
    }
    :param session_token: str A session token
    :return: dict The session record
    """
    mc = get_memcache()
    session_record = mc.get(_get_session_record_id(session_token))
    return _deserialize_session_record(session_record)


def new(party_id: int, party_type: PartyTypes=PartyTypes.DataClient, ttl: int=1800) -> Optional[str]:
    """
    Inserts a new session record for the party.
    Also pins the session to the clients IP to help with mitm attacks on session
    tokens.
    :param party_type: PartyTypes The type of Party whose session this is
    :param party_id: str The uuid of the associated party
    :param ttl: int Optional maximum time without activity before logout
    :return: bool Session token
    """
    session_token = os.urandom(g._config['AUTH_SESSION_TOKEN_LENGTH']).hex()
    while is_valid(session_token):
        session_token = os.urandom(g._config['AUTH_SESSION_TOKEN_LENGTH']).hex()

    assert type(ttl) == int
    session_record = _build_session_record(party_id, party_type, ttl)
    debug_print("Auth: Inserting session record {}".format(session_record))

    mc = get_memcache()
    if mc.set(_get_session_record_id(session_token), session_record) != 0:
        return session_token

    return None


def invalidate(session_token: str) -> bool:
    """
    Invalidates a session token by removing it from memcached.
    :param session_token: str A valid session token
    :return: bool success
    """
    mc = get_memcache()
    return mc.delete(_get_session_record_id(session_token)) != 0


def validate_activity(session_token: str) -> bool:
    """
    Refreshes the last_seen timestamp for the given token.
    Also removes old sessions (auto logout)
    Raises ClientIpChangedException if client's ip address changed since last
    activity (possible mitm)
    :param session_token: str A valid session token
    :return: bool Success
    """
    if not is_valid(session_token):
        debug_print('Auth: Session token is not valid: {}'.format(session_token))
        return False

    session_record = get_session_record(session_token)

    if session_record['client_ip'] != get_client_ip():
        raise ClientIpChangedException("IP was {}, but is {} now".format(
            session_record['client_ip'], get_client_ip()))

    session_record['last_seen'] = time.time()

    mc = get_memcache()
    key = _get_session_record_id(session_token)
    return mc.replace(key, _serialize_session_record(session_record)) != 0


def is_valid(session_token: str) -> bool:
    """
    Returns a bool indicating whether the given session token is valid.
    A session token is valid if:
        1) someone has logged in and the token was handed out to them AND
        2) the timedelta from the last activity with this token to now doesn't
           exceed the session ttl AND
        3) the token wasn't revoked (by logging out a user)
    Having a valid session token means you're allowed to do stuff
    However, this method should not be used to manually check if the current
    client has permissions, as it doesn't do IP pinning.
    Token validation is done automatically before each request is processed and
    if a client is accessing without permissions, the API automatically
    redirects.
    :param session_token: A session token
    :return: bool
    """
    if type(session_token) != str:
        raise TypeError

    session_record = get_session_record(session_token)

    if session_record is None:
        debug_print('Auth: No session record found in MC.')
        return False

    if time.time() - session_record['last_seen'] > session_record['ttl']:
        invalidate(session_token)
        debug_print('Auth: Session token expired: {}'.format(session_token))
        return False

    return True


def who_is(session_token: str) -> Optional[int]:
    """
    Returns the Party uuid for the given session_token.
    :param session_token: str A session token
    :return: str the uuid
    """
    if not is_valid(session_token):
        return None

    session_record = get_session_record(session_token)
    return session_record['uuid']


def logout():
    """
    Logs out the current user, raises UserNotLoggedInException if the session is already invalid.
    :return: None
    """
    if g._current_user is None:
        raise UserNotLoggedInException()

    if not invalidate(g._current_session_token):
        raise UserNotLoggedInException()


def current_user() -> "Party":
    return g._current_user