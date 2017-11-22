import time

from framework.exceptions import ClientIpChangedException
from framework.memcached import get_memcache
from framework import get_client_ip
from model import DataClient

_memcached_prefix = "auth."


def _get_session_record_id(session_token: str) -> str:
    """
    Returns the name of the key used in memcached to identify the session record with the given session_token
    :param session_token: str A session token
    :return: str
    """
    return _memcached_prefix + "sessions." + session_token


def _get_session_record(session_token: str) -> dict:
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
    return mc.get(_get_session_record_id(session_token))


def new_session(session_token: str, client_uuid: str, ttl: int=1800) -> bool:
    """
    Inserts a new session record for the given session token.
    Only works if token has no record yet.
    Also pins the session to the clients IP to help with mitm attacks on session tokens.
    :param session_token: str A session token that hasn't been used yet
    :param client_uuid: str The uuid of the associated DataClient
    :param ttl: int Optional maximum time without activity before logout
    :return: bool Success
    """
    if is_valid(session_token):
        return False

    if not type(client_uuid) == str:
        return False

    if not type(ttl) == int:
        return False

    session_record = {
        'uuid': client_uuid,
        'ttl': ttl,
        'last_seen': time.time(),
        'client_ip': get_client_ip()
    }

    mc = get_memcache()
    return mc.set(_get_session_record_id(session_token), session_record)


def invalidate(session_token: str) -> bool:
    """
    Invalidates a session token by removing it from memcached.
    :param session_token: str A valid session token
    :return: bool success
    """
    mc = get_memcache()
    return mc.delete(_get_session_record_id(session_token))


def activity(session_token: str) -> bool:
    """
    Refreshes the last_seen timestamp for the given token.
    Also removes old sessions (auto logout)
    Raises ClientIpChangedException if client's ip address changed since last activity (possible mitm)
    :param session_token: str A valid session token
    :return: bool Success
    """
    if not is_valid(session_token):
        return False

    session_record = _get_session_record(session_token)

    if session_record['client_ip'] != get_client_ip():
        raise ClientIpChangedException("IP was {}, but is {} now".format(session_record['client_ip'], get_client_ip()))

    session_record['last_seen'] = time.time()


    mc = get_memcache()
    return mc.replace(_get_session_record_id(session_token), session_record)


def is_valid(session_token: str) -> bool:
    """
    Returns a bool indicating whether the given session token is valid.
    A session token is valid if:
        1) someone has logged in and the token was handed out to them AND
        2) the timedelta from the last activity with this token to now doesn't exceed the session ttl AND
        3) the token wasn't revoked (by logging out a user)
    Having a valid session token means you're allowed to do stuff
    However, this method should not be used to manually check if the current client has permissions, as it doesn't do
    IP pinning. Token validation is done automatically (TODO: implement) before each request is processed and if
    a client is accessing without permissions, the API automatically redirects.
    :param session_token: A session token
    :return: bool
    """
    if type(session_token) != str:
        raise TypeError

    session_record = _get_session_record(session_token)

    if not session_record:
        return False

    if time.time() - session_record['last_seen'] > session_record['ttl']:
        invalidate(session_token)
        return False

    return True


def who_is(session_token: str) -> str:
    """
    Returns the DataClient uuid for the given session_token.
    :param session_token: str A session token
    :return: str the uuid
    """
    if not is_valid(session_token):
        return None

    session_record = _get_session_record(session_token)
    return session_record['uuid']
